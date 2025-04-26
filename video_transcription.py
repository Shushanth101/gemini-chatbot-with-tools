from youtube_transcript_api import YouTubeTranscriptApi

def transcribe_yt_video(video_id:str)-> str:
    ytt_api = YouTubeTranscriptApi()
    fetched_transcript = ytt_api.fetch(video_id)
    full_text=""
    for snippet in fetched_transcript:
        full_text += snippet.text
    return full_text

if __name__ =="__main__":


    transcribe_yt_video("jeCDCbqqmes")
