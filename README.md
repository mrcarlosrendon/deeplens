# deeplens
Code for DeepLens Challenge

## Inspiration

Getting my badge scanned awkwardly at re:Invent conference. Didn't we just get magical cameras that solve all problems?

## What it does

Tracks who comes to your booth using badge photos to identify conference participants. Not only that, it tracks how long they stay at your booth, and if they opened their mouths. Meaning that it conveys some information about the quality of the interactions, not just the amount.

## How I built it
1. Identify presence of faces in video stream
2. Match individual faces using AWS Rekognition and submitted conference badge photos as well as capture emotions and mouth position.
3. Store information about the faces in a database indexed by time
4. Artfully present the information to the booth owner

## Challenges I ran into

Camera placement, and crowding pose challenges for real-world use. Still I want to believe.

## Accomplishments that I'm proud of

- I got the DeepLens to work at all.
- The submission actually works.

## What I learned

## What's next for BoothLens

Start a company to promote technology. Or since I'm lazy, just demo the thing when I have an excuse.
