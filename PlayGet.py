
import requests

KEY = "MKXQATZ9XR0Mc2dJDyw01Q"
isbns = 9781632168146
searchword = "Harry"

def main(KEY,isbns):
    resReview = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": KEY, "isbns": isbns})
    print(resReview.text)

def getBasicInfo(isbns):
    GetGoodreadID = requests.get("https://www.goodreads.com/book/isbn_to_id.json", params={"isbns": isbns})

    basicInfo = requests.get("https://www.goodreads.com/book/show.json", params={"GetGoodreadID ": GetGoodreadID })
    print(basicInfo.text)

def search(KEY, searchword):
    resSearch = requests.get("https://www.goodreads.com//search/index.xml",
                             params={"q":searchword,"key": KEY})
    print(resSearch.text)

if __name__ == "__main__":
    main(KEY, isbns)
    getBasicInfo(isbns)

    #search(KEY, searchword)