import urllib.request, urllib.parse, urllib.error
import json
import ssl
import pafy
import vlc

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

api_key = 'AIzaSyDXEEu3hkBznF3uhUUtTCRu4ayt84Vb0AM'
service_url ='https://www.googleapis.com/youtube/v3/search?'
#url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&order=viewCount&q=skateboarding%20dog&type=video&videoDefinition=high&key=[YOUR_API_KEY]'


while True:
    song = input('Enter song description: ')
    parms = dict()
    parms['part']='snippet'
    parms['q'] = song
    parms['type']='video'
    parms['maxResults']='10'

    if api_key is not False: parms['key'] = api_key
    url = service_url + urllib.parse.urlencode(parms)

    print('Retrieving', url)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters')

    try:
        js = json.loads(data)
    except:
        js = None
    #print(json.dumps(js, indent=4))
    # #js = json.dumps(js, indent=4)

    track = js['items'][0]
    title = track['snippet']['title']
    link = track['id']['videoId']
    print(title)
    print('https://www.youtube.com/watch?v='+link)
    v = pafy.new('https://www.youtube.com/watch?v='+link)
    print('Title -',v.title)
    print('Duration -',v.duration)
    print('rating -',v.rating)
    print('source -',v.author)
    #print(v.length)
    # print(v.keywords)
    # print(v.thumb)
    # print(v.videoid)
    print('Popularity-',v.viewcount)

    a = v.getbestaudio(preftype='any')

    print('Quality-',a.bitrate)
    print(a.extension)
    a.download()


    string_path = title+'.'+a.extension
    print("Playing"+" "+"./"+string_path)
    player = vlc.MediaPlayer("./"+string_path)
    print(player)
    player.play()
    next_act = input("Press stop to close & next to play next song\n")
    if next_act=='stop':
        player.stop()
        break
    if next_act=='next':
        player.stop()
        continue