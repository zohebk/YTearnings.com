# Video 1 : 
This code is a Python script that helps you find popular YouTube videos based on a topic you provide. It also estimates how much money each video might earn. The code uses Google's YouTube API to search for videos and Gradio, a library that helps create a web interface for the script. 

Here's a simple explanation of what each part of the code does:

1. Import necessary libraries: The code starts by importing libraries that provide helpful tools like connecting to the YouTube API and creating the web interface.
2. API Key: You need an API key to connect to the YouTube API. The API key in the code is just an example, and you should replace it with your own.
3. build_youtube_service(): This function builds a connection to the YouTube API using your API key.
4. categorize_niche(): This function looks at the video's title and description to determine if it belongs to a high-paying, medium-paying, or low-paying niche. It does this by looking for specific keywords in the title and description.
5. calculate_earnings(): This function estimates how much a video might earn based on its views, language, and niche. It uses a dictionary that contains earnings per 1000 views for different languages and niches.
6. get_trending_videos(): This function searches for videos on YouTube based on the topic you provide. It gathers important data like view count, like count, and video language.
7. format_metric() and format_earnings(): These functions help to format the numbers in a more readable way, like converting large numbers into thousands (K), millions (M), or billions (B).
8. app(): This is the main function that ties everything together. It takes your input (topic, maximum results, etc.) and calls the get_trending_videos() function to get the videos. Then, it calculates the estimated earnings for each video and formats the data into a nice-looking table.
9. Gradio Interface: Finally, the code creates a web interface using Gradio. It allows you to enter your input and see the results in your web browser.
In summary, this code lets you search for popular YouTube videos based on a topic and estimates their earnings. It connects to the YouTube API, processes the data, and presents it in an easy-to-read table through a web interface.
