from bitly import Bitly

token = 'c9686d338251d133c9ad14192e7649312fd58cef'
group_uid = 'Bn279omU00d'

long_url = 'https://t.me/TG747_AG_BOT?start=98'

if __name__ == '__main__':
    bitly = Bitly(token=token, group_uid=group_uid)

    # create links for DM
    links_dm = bitly.gen_links(long_url, 6, tags=['dm'])

    # create links for Qingtian
    links_qingtian = bitly.gen_links(long_url, 2, tags=['Qingtian'])

    # save links to csv
    bitly.save_links([links_dm, links_qingtian], filename='98')

    # get clicks summary
    params = (
        ('tags', ['dm', 'Qingtian']),
    )
    clicks = bitly.get_links_clicks(params)
    print(clicks)