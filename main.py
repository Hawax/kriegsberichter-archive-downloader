import requests
from lxml import html
import os
import time

list_of_numbers = []
# making list of ids
for i in range(1, 11):
    list_of_numbers.append('00'+str(i))
for i in range(10, 101):
    list_of_numbers.append('0'+str(i))
for i in range(100, 1001):
    list_of_numbers.append(str(i))
for i in range(1000, 10001):
    list_of_numbers.append(str(i))


def open_connetion(link):
    try:
        r = requests.get(link)
        return r
    except:
        print(link, '- this link has been blocked.')
        print('Waiting 5 seconds...')
        time.sleep(5)
        return open_connetion(link)


def clean_dirname(dirname):
    for symbol in ["/", "\\", ":", ":", "*", "<", ">", "|", '"', ",", "?", '=']:
        dirname = dirname.replace(symbol, '')
    return dirname


def get_list_of_sites(_r):
    tree = html.fromstring(_r.content)
    for i in range(1, 8):
        try:
            number = tree.xpath("//div[@class='navigationBar']/a[{}]".format(str(i)))[0].text_content()
        except IndexError:
            #print(i)
            number = tree.xpath("//div[@class='navigationBar']/a[{}]".format(str(i-1)))
            try:
                return int(str(number[0].text_content()))
            except:
                return 1


def get_hrefs(_r):
    links = []
    tree = html.fromstring(_r.content)
    for i in range(1, 16):
        xpath = "//li[{}]/span[1]/span[@class='wrap2' and 1]/a[1]".format(i)
        try:
            href = tree.xpath(xpath)[0].get("href")
        except IndexError:
            break

        links.append("http://www.kriegsberichter-archive.com/" + href)
    return links


def get_img_url_and_name(_r):
    tree = html.fromstring(_r.content)
    xpath = "//img[@id='theMainImage']"
    href = tree.xpath(xpath)[0].get("src")
    name = tree.xpath(xpath)[0].get("alt")
    print('http://www.kriegsberichter-archive.com/' + href, name)
    return 'http://www.kriegsberichter-archive.com/'+ href, name


def skip(listdir, list_of_numbers_):
    """Just skip existing files"""
    how_many_to_skip = 0
    for world in listdir:
        world = world.replace('.jpg', '')
        world = world.split('_')

        for id in list_of_numbers_:
            if id in world[-1]:
                how_many_to_skip += 1
    if how_many_to_skip:
        print(how_many_to_skip,'- skip')
    return (how_many_to_skip)


def main(_r):
    tree = html.fromstring(_r.content)
    try:os.mkdir('photos')
    except: pass

    for i in range(1, 90):
        title = tree.xpath("//li[{}]/div[@class='thumbnailCategory' and 1]/div[@class='description' and 2]/h3[1]/a[1]".format(str(i)))
        title_url = tree.xpath(
            "//li[{}]/div[@class='thumbnailCategory' and 1]/div[@class='description' and 2]/h3[1]/a[1]".format(str(i)))[0].get('href')
        title_url = 'http://www.kriegsberichter-archive.com/{}'.format(title_url)
        title = clean_dirname(title[0].text_content())
        print(title)
        path = 'photos\\{}'.format(title)

        try:os.mkdir(path)
        except: pass

        listdir_ = os.listdir(path)

        print(i,'- section')
        r = open_connetion(title_url)

        how_much_sites = get_list_of_sites(r)
        print(how_much_sites, 'How much sites')

        os.listdir(path)
        how_many_to_skip = skip(listdir_, list_of_numbers)
        for j in range(0, how_much_sites+1):
            print(str(j),'/',how_much_sites,'- so much left to the end ', i, '- sections')

            r = open_connetion(title_url+"/"+'start-{}'.format(str(j*15)))
            links_of_photo= get_hrefs(r)

            for numer, link in enumerate(links_of_photo, 0):

                if how_many_to_skip and not title == 'WeillSS-Kriegsberichter': # WeillSS-Kriegsberichter there are
                    how_many_to_skip -= 1                                       # two WeillSS-Kriegsberichter folders so we dont want to skip this photos
                    continue

                r = open_connetion(link)
                url, name = get_img_url_and_name(r)
                url_direct = open_connetion(url)

                with open(path + '\\'+name, 'wb') as file:
                    file.write(url_direct.content)
                    file.close()


if __name__ == '__main__':
    r = open_connetion('http://www.kriegsberichter-archive.com/index.php')
    main(r)
