import requests

def get_web_content(link:str)->str:
    base_url = "https://r.jina.ai"
    response = requests.get(base_url+"/"+link)
    if response.status_code == 200 :
        return response.text
    else :
        return "some error ocurred"

if __name__ == "__main__":
    print(get_web_content("https://cloud.google.com/docs/ai-ml"))