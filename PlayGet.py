
import requests

KEY = "MKXQATZ9XR0Mc2dJDyw01Q"
isbns = 9781632168146
searchword = "Harry"

def main(KEY,isbns):
    resReview = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": KEY, "isbns": isbns})
    print(resReview.text)

def getBasicInfo(KEY, isbns):
    basicInfo = requests.get("https://www.goodreads.com/book/show.json", params={"format": "json","""key": KEY, "GetGoodreadID ": GetGoodreadID })
    print(basicInfo)
    return basicInfo


def search(KEY, searchword):
    resSearch = requests.get("https://www.goodreads.com//search/index.xml",
                             params={"q":searchword,"key": KEY})
    print(resSearch.text)

if __name__ == "__main__":

    main(KEY,isbns)
    getBasicInfo(KEY, isbns)


    #search(KEY, searchword)