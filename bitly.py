import json
import requests
import pandas as pd


class Bitly:

    def __init__(self, token: str, group_uid: str):
        self.headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        self.group_uid = group_uid

    def gen_links(self,
                  long_url: str,
                  n: int = 1,
                  tags: list[str] = []) -> pd.DataFrame:

        tags = tags if tags else ['base']
        tags_key = '/'.join(tags)

        # create links
        links = []
        for j in range(1, n + 1):
            url = f"{long_url}&utm_content={j}"
            data = {"long_url": url, "domain": "bit.ly", 'tags': tags}
            data = json.dumps(data)

            response = requests.post('https://api-ssl.bitly.com/v4/bitlinks', headers=self.headers, data=data)
            self.check_response(response)

            result = response.json()
            links.append((result['link'], tags_key))

            print(result, end='\n\n')

        return pd.DataFrame(links, columns=['link', 'tag'])

    def get_links_clicks(self, params):
        # get all the links
        response = requests.get(f'https://api-ssl.bitly.com/v4/groups/{self.group_uid}/bitlinks',
                                headers=self.headers,
                                params=params)
        self.check_response(response)

        links = response.json()['links']

        # get clicks summary
        clicks_summary = []
        for link in links:
            response = requests.get(f"https://api-ssl.bitly.com/v4/bitlinks/{link['id']}/clicks/summary",
                                    headers=self.headers, params=params)
            self.check_response(response)

            clicks = response.json()['total_clicks']
            clicks_summary.append((link['id'], '/'.join(link['tags']), clicks))

        return pd.DataFrame(clicks_summary, columns=['link', 'tag', 'clicks'])

    @staticmethod
    def check_response(response):
        if response.status_code not in (200, 201):
            msg = f'{response.status_code} - {response.reason}' + '\n\n'
            msg += f'{response.url}' + '\n\n'
            msg += f'{response.text}'

            raise ValueError(msg)

    @staticmethod
    def save_links(data, filename) -> None:
        if isinstance(data, (list, tuple)):
            data = pd.concat(data)

        data.to_csv(f'{filename}.csv', index=False)