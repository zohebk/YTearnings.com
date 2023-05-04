import gradio as gr
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
from datetime import datetime
import os
import re
import platform

API_KEY = os.environ.get('YOUTUBE_API_KEY')
def build_youtube_service():
    return build("youtube", "v3", developerKey=API_KEY)

def categorize_niche(title, description):
    high_paying_keywords = [
        "insurance", "loans", "mortgage", "attorney", "credit", "software",
        "degree", "hosting", "claim", "donate", "conference call", "trading",
        "online courses", "real estate", "marketing", "finance", "tech"
    ]

    medium_paying_keywords = [
        "health", "fitness", "travel", "beauty", "fashion", "cooking",
        "lifestyle", "gaming", "sports", "home improvement", "gardening",
        "pets", "parenting", "education", "career"
    ]

    # Combine title and description for keyword analysis
    text = title.lower() + " " + description.lower()

    # Check for high-paying keywords
    for keyword in high_paying_keywords:
        if re.search(r'\b' + keyword + r'\b', text):
            return "high"

    # Check for medium-paying keywords
    for keyword in medium_paying_keywords:
        if re.search(r'\b' + keyword + r'\b', text):
            return "medium"

    # Default to low-paying niche
    return "low"

def calculate_earnings(views, language, niche):
    earnings_per_1000_views = {
        "high": {
            "en-US": 4.5,
            "en": 4.5,
            "af": 3.2,
            "ar": 2.0,
            "az": 1.5,
            "be": 1.8,
            "bg": 1.6,
            "bn": 1.2,
            "ca": 3.5,
            "cs": 2.5,
            "da": 2.8,
            "de": 2.0,
            "el": 2.2,
            "en-GB": 3.2,
            "en-AU": 2.8,
            "en-CA": 3.5,
            "es": 2.0,
            "et": 1.6,
            "fa": 1.2,
            "fi": 2.5,
            "fil": 2.0,
            "fr": 2.5,
            "gl": 1.8,
            "gu": 1.2,
            "hi": 1.2,
            "hr": 2.2,
            "hu": 2.2,
            "hy": 1.5,
            "id": 1.0,
            "is": 1.8,
            "it": 2.0,
            "iw": 2.5,
            "ja": 2.0,
            "ka": 1.5,
            "kk": 1.2,
            "km": 1.0,
            "kn": 1.2,
            "ko": 1.5,
            "ky": 1.0,
            "lo": 0.8,
            "lt": 1.6,
            "lv": 1.6,
            "mk": 1.5,
            "ml": 1.0,
            "mn": 1.5,
            "mr": 1.0,
            "ms": 1.0,
            "my": 1.0,
            "ne": 0.8,
            "nl": 2.2,
            "no": 2.5,
            "pl": 1.8,
            "pt": 1.8,
            "ro": 1.6,
            "ru": 1.8,
            "si": 1.0,
            "sk": 2.0,
            "sl": 2.0,
            "sq": 1.2,
            "sr": 2.2,
            "sv": 2.5,
            "sw": 1.0,
            "ta": 1.0,
            "te": 1.0,
            "th": 1.2,
            "tr": 1.5,
            "uk": 1.8,
            "ur": 2.2,
            "uz": 1.0,
            "vi": 1.0,
            "zh-CN": 1.5,
            "zh-HK": 1.8,
            "zh-TW": 1.5,
            "hi-Latn": 1.0,
            "": 2.0  # Default earnings per 1000 views
        },
    "medium": {
            "en-US": 2.5,
            "en": 2.5,
            "fr": 2.0,
            "es": 1.8,
            "de": 1.8,
            "it": 1.5,
            "pt": 1.5,
            "nl": 1.4,
            "pl": 1.2,
            "tr": 1.2,
            "ru": 1.0,
            "ar": 0.8,
            "hi": 0.8,
            "ja": 1.2,
            "ko": 1.0,
            "zh-CN": 1.0,
            "zh-TW": 1.0,
            "": 1.2  # Default earnings per 1000 views
        },
        "low": {
            "en-US": 1.2,
            "en": 1.2,
            "fr": 0.8,
            "es": 0.7,
            "de": 0.7,
            "it": 0.6,
            "pt": 0.6,
            "nl": 0.5,
            "pl": 0.5,
            "tr": 0.4,
            "ru": 0.4,
            "ar": 0.3,
            "hi": 0.3,
            "ja": 0.5,
            "ko": 0.4,
            "zh-CN": 0.4,
            "zh-TW": 0.4,
            "": 0.5  # Default earnings per 1000 views
        }
    }

    language = language.lower().replace('_', '-')
    niche_earnings = earnings_per_1000_views.get(niche.lower(), earnings_per_1000_views["high"])
    return views * (niche_earnings.get(language, niche_earnings[""]) / 1000)
    return earnings

def get_trending_videos(topic, max_results=10, search_transcript=False, upload_date=None, country=None, language=None):
    service = build_youtube_service()

    try:
        query = topic + (' intitle:"Transcript"' if search_transcript else '')
        search_response = service.search().list(
            part="id,snippet",
            q=query,
            type="video",
            videoDefinition="high",
            order="viewCount",
            maxResults=max_results,
            fields="items(id(videoId),snippet(publishedAt,channelTitle,title,channelId))",
        ).execute()

        videos = []
        for search_result in search_response.get("items", []):
            video_id = search_result["id"]["videoId"]
            channel_id = search_result["snippet"]["channelId"]
            video_response = service.videos().list(
                part="statistics,snippet",
                id=video_id,
                fields="items(statistics(viewCount),statistics(likeCount),statistics(dislikeCount),statistics(commentCount),snippet(defaultAudioLanguage))"
            ).execute()
            channel_response = service.channels().list(
                part="statistics",
                id=channel_id,
                fields="items(statistics(subscriberCount))"
            ).execute()
            video_description = service.videos().list(
                part="snippet",
                id=video_id,
                fields="items(snippet(description))"
            ).execute()

            view_count = 0
            if "viewCount" in video_response["items"][0]["statistics"]:
                view_count = video_response["items"][0]["statistics"]["viewCount"]

            like_count = 0
            if "likeCount" in video_response["items"][0]["statistics"]:
                like_count = video_response["items"][0]["statistics"]["likeCount"]

            dislike_count = 0
            if "dislikeCount" in video_response["items"][0]["statistics"]:
                dislike_count = video_response["items"][0]["statistics"]["dislikeCount"]

            comment_count = 0
            if "commentCount" in video_response["items"][0]["statistics"]:
                comment_count = video_response["items"][0]["statistics"]["commentCount"]

            subscriber_count = channel_response["items"][0]["statistics"]["subscriberCount"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            published_at = datetime.fromisoformat(search_result["snippet"]["publishedAt"].rstrip("Z")).strftime(
                "%Y-%m-%d %H:%M:%S")
            video_language = video_response["items"][0]["snippet"].get("defaultAudioLanguage", "Unknown")
            description = video_description["items"][0]["snippet"]["description"]

            videos.append({
                "Video URL": video_url,
                "Published At": published_at,
                "Channel Title": search_result["snippet"]["channelTitle"],
                "Title": search_result["snippet"]["title"],
                "Views": int(view_count),
                "Likes": int(like_count),
                "Dislikes": int(dislike_count),
                "Comments": int(comment_count),
                "Subscribers": int(subscriber_count),
                "Language": video_language,
                "Description": description
            })

        df = pd.DataFrame(videos)
        return df

    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")
        return None



def format_metric(n):
    if n < 1000:
        return str(n)
    elif n < 1000000:
        result = f"{n/1000:.1f}"
        if result.endswith(".0"):
            result = result[:-2]
        return result + "K"
    elif n < 1000000000:
        result = f"{n/1000000:.1f}"
        if result.endswith(".0"):
            result = result[:-2]
        return result + "M"
    elif n < 1000000000000:
        result = f"{n/1000000000:.1f}"
        if result.endswith(".0"):
            result = result[:-2]
        return result + "B"
    else:
        result = f"{n/1000000000000:.1f}"
        if result.endswith(".0"):
            result = result[:-2]
        return result + "T"



def format_earnings(earnings):
    return f"${earnings:.2f}"

def getHtml():
    # Define the Clarity tracking code as an environment variable
    CLARITY_CODE = os.environ.get('CLARITY_CODE')

    # Define the HTML template for the interface
    html_template = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>My Gradio App</title>
            <script type="text/javascript">
                (function(c,l,a,r,i,t,y){{
                    c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
                    t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
                    y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
                }})(window, document, "clarity", "script", "{CLARITY_CODE}");
            </script>
        </head>
        <body>
            <h1>My Gradio App</h1>
            <p>This is my app that does something useful.</p>
            $input_section
            <hr>
            $output_section
        </body>
    </html>
    """
    return html_template


def app(topic, max_results,  upload_date=None, date_operator=None, country=None, language=None):
    if not upload_date:
        upload_date = datetime.today().strftime('%Y-%m-%d')
    search_transcript = None
    results = get_trending_videos(topic, max_results, search_transcript, upload_date, country, language)
    if results is not None and not results.empty:
        # Convert datetime.date to datetime.datetime for formatting
        if "Published At" in results:
            results["Published At"] = pd.to_datetime(results["Published At"])

        # Apply datetime format to date columns
        for col in ["Published At"]:
            if col in results:
                results[col] = results[col].apply(lambda x: datetime.strftime(x, "%Y-%m-%d"))

        # Filter by upload date
        if upload_date is not None and date_operator is not None:
            upload_date = datetime.strptime(upload_date, "%Y-%m-%d").date()
            if date_operator == "greater_than":
                results = results[results["Published At"] > upload_date.strftime("%Y-%m-%d")]
            elif date_operator == "less_than":
                results = results[results["Published At"] < upload_date.strftime("%Y-%m-%d")]

        # Add Niche
        results["Niche"] = results.apply(lambda x: categorize_niche(x["Title"], x["Description"]), axis=1)

        # Add Earnings column
        results["Est.Earnings"] = results.apply(lambda x: calculate_earnings(x["Views"], x["Language"], x["Niche"]), axis=1)
        # Format Earnings column
        results["Est.Earnings"] = results["Est.Earnings"].apply(lambda x: "${:,.1f}".format(x))

        # Apply format_metric to Views and Subscribers columns
        results["Likes"] = results["Likes"].apply(format_metric)
        if not results["Comments"].isnull().all():
            results["Comments"] = results["Comments"].apply(format_metric)
        else:
            results["Comments"] = 0
        results["Views"] = results["Views"].apply(format_metric)
        results["Subscribers"] = results["Subscribers"].apply(format_metric)

        # Make the "Video URL" column clickable
        results['Video URL'] = results['Video URL'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')

        # Save DataFrame as CSV
        csv_file = "trending_videos.csv"
        results.to_csv(csv_file, index=False)

        # Drop Description and Niche columns
        results = results.drop(["Description", "Niche", "Comments", "Likes", "Language", "Subscribers", "Dislikes"], axis=1)
        
        # Convert DataFrame to HTML table
        html_table = results.to_html(index=False, classes=["table", "table-striped", "table-bordered", "table-hover"], escape=False)

        return html_table, csv_file

    elif results is not None and results.empty:
        return "No results found. Please try different search criteria.", None

    else:
        return "An error occurred while fetching the data. Please try again.", None



inputs = [
    gr.inputs.Textbox(label="Search"),
    gr.inputs.Slider(minimum=1, maximum=50, default=10, label="Max Results"),
    gr.inputs.Textbox(label="Upload Date Filter (YYYY-MM-DD)"),
    gr.inputs.Dropdown(label="Date Comparison Operator", choices=["", "greater_than", "less_than"])
]
outputs=[
        gr.outputs.HTML(label="Results"),
        gr.outputs.File(label="Download CSV")
    ]

inputs = [
    gr.inputs.Textbox(label="Search"),
    gr.inputs.Slider(minimum=1, maximum=50, default=10, label="Max Results"),
    gr.inputs.Checkbox(label="Search in video transcript"),
    gr.inputs.Textbox(label="Upload Date Filter (YYYY-MM-DD)"),
    gr.inputs.Dropdown(label="Date Comparison Operator", choices=["", "greater_than", "less_than"]),
]


iface = gr.Interface(
    fn=app,
    inputs=inputs,
    outputs=[
        gr.outputs.HTML(label="Results"),
        gr.outputs.File(label="Download CSV")
    ],
    title="Top YouTube Videos, Ordered by View and Estimated Earnings",
    description="Enter a search and click 'Submit'. Use quotes like 'Barack Obama' for search to get specific results",
    flagging=False,
    theme="compact",
    html = getHtml()
)

iface.launch(inbrowser=True) 

