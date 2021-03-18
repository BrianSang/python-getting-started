from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import os
import requests
import threading
import json
import random

import hashlib, hmac

API_TOKEN = b'4a75b7fb787a3f6b57c4e63050003d619febd82c'

@csrf_exempt
def index(request):
    headers = request.headers
    print("header: " + str(headers))

    if request.method == 'GET':
        return HttpResponse('Received GET')
    elif request.method == 'POST':
        print("Received POST")

        body_unicode = request.body.decode('utf-8')
        webhook_payload = json.loads(body_unicode)
        print("webhook_payload: " + str(webhook_payload))

        category = webhook_payload['category']
        app_id = webhook_payload['app_id']
        channel_url = webhook_payload['channel']['channel_url']

        print("app_id: " + app_id)
        print("channel_url: " + channel_url)

        x_sendbird_signature = headers['X-Sendbird-Signature']
        print("x_sendbird_signature: " + x_sendbird_signature)
        validate_X_Sendbird_Signature(x_sendbird_signature, body_unicode)

        thread = threading.Thread(target=sendAdminMessage, args=(category, app_id, channel_url))
        thread.start()

        return HttpResponse('Hello webhook!')


def validate_X_Sendbird_Signature(x_sendbird_signature, body_unicode):
    signature_to_compare = hmac.new(
        key=API_TOKEN,
        #msg=bytes(body_unicode.encode('utf8')),
        msg=bytes(body_unicode),
        digestmod=hashlib.sha256).hexdigest()

    print("signature_to_compare: " + signature_to_compare)

    assert signature_to_compare == x_sendbird_signature, "x_sendbird_signature is NOT correct!"


def sendAdminMessage(category, app_id, channel_url):
    URL = "https://api-" + app_id + ".sendbird.com/v3/group_channels/" + channel_url + "/messages"
    headers = {"Content-Type": "application/json; charset=utf8", "Api-Token": API_TOKEN}

    if category == "group_channel:create":
        (quote, author) = selectQuote()
        data = {"message_type": "ADMM", "message": quote, "data": "Author: " + author}
        res = requests.post(URL, headers=headers, data=json.dumps(data))
        print("response: " + res.text)
    elif category == "group_channel:message_delete":
        data = {"message_type": "ADMM", "message": "Message deleted"}
        res = requests.post(URL, headers=headers, data=json.dumps(data))
        print("response: " + res.text)


def selectQuote():
    quotes = [
        ["You know, Hobbes, some days even my lucky rocketship underpants don't help.", "Bill Watterson"],
        ["Even if we don't have the power to choose where we come from, we can still choose where we go from there.",
         "Stephen Chbosky"],
        ["And now that you don't have to be perfect, you can be good.", "John Steinbeck"],
        [
            "Outside the windows the day was bright: golden sunshine, blue sky, pleasant wind... I wanted to punch "
            "the happy day in the face, grab it by the hair, and beat it until it told me what the hell it was so "
            "happy about.",
            "Ilona Andrews"],
        [
            "I haven't had a very good day. I think I might still be hungover and everyone's dead and my root beer's "
            "gone.",
            "Holly Black"],
        [
            "It is impossible to live without failing at something, unless you live so cautiously that you might as "
            "well not have lived at all - in which case, you fail by default.",
            "J.K. Rowling"],
        ["But I am very poorly today & very stupid & I hate everybody & everything. One lives only to make blunders.",
         "Charles Darwin"],
        [
            "We are cups, constantly and quietly being filled. The trick is knowing how to tip ourselves over and let "
            "the beautiful stuff out.",
            "Ray Bradbury"],
        [
            "You may encounter many defeats, but you must not be defeated. In fact, it may be necessary to encounter "
            "the defeats, so you can know who you are, what you can rise from, how you can still come out of it.",
            "Maya Angelou"],
        ["Life is never fair, and perhaps it is a good thing for most of us that it is not.", "Oscar Wilde"],
        [
            "Maybe it’s not about having a beautiful day, but about finding beautiful moments. Maybe a whole day is "
            "just too much to ask. I could choose to believe that in every day, in all things, no matter how dark and "
            "ugly, there are shards of beauty if I look for them.",
            "Anna White"],
        ["I've had the sort of day that would make St. Francis of Assisi kick babies.", "Douglas Adams"],
        ["Don't cry because it's over. Smile because it happened.", "Dr. Seuss"],
        ["Everything is hard before it is easy.", "Johann Wolfgang von Goethe"],
        ["Anyone who has never made a mistake has never tried anything new.", "Albert Einstein"],
        [
            "These worst mornings with cold floors and hot windows and merciless light ? the soul's certainty that "
            "the day will have to be not traversed but sort of climbed, vertically, and then that going to sleep "
            "again at the end of it will be like falling, again, off something tall and sheer.",
            "David Foster Wallace"],
        ["Don't let your happiness depend on something you may lose.", "C.S. Lewis"],
        [
            "It's so hard to forget pain, but it's even harder to remember sweetness. We have no scar to show for "
            "happiness. We learn so little from peace.",
            "Chuck Palahniuk"],
        ["We are all broken, that's how the light gets in.", "Ernest Hemingway"],
        ["Monsters are real, ghosts are real, too. They live inside us, and sometimes they win.", "Stephen King"]
    ]
    return quotes[random.randint(0, 19)]