import openai
openai.api_key = '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'
response = openai.Image.create_edit(
  image=open("/Users/narendra/Rakathon/Images/rakathon/bed/bed2.png", "rb"),
  mask=open("/Users/narendra/Rakathon/Images/rakathon/bed/bed2.png", "rb"),
  prompt="Mask other content except the bed, don't change bed color or any bed properties",
  n=1,
  size="1024x1024"
)
image_url = response['data'][0]['url']
print(image_url)