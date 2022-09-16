# Queen Queue Length Plotter

# Author: Michael Grace <github.com/michael-grace>

from dataclasses import dataclass
import datetime
import snscrape.modules.twitter as sntwitter
import matplotlib.pyplot as plt
import matplotlib.dates

tweets = []


@dataclass
class QueueUpdate():
    time: datetime.datetime
    tweet_content: str

    @property
    def queue_length(self) -> float:
        lines = self.tweet_content.split("\n")
        candidates = [x for x in lines if "Distance" in x]
        return float(candidates[0].split()[1])


@dataclass
class AtCapacityQueueElement():
    time: datetime.datetime
    queue_length: float = 8


for tweet in sntwitter.TwitterSearchScraper("from:QE2Queue").get_items():
    if "Distance" in tweet.content:
        tweets.append(QueueUpdate(
            tweet.date,
            tweet.content
        ))
    else:
        tweets.append(AtCapacityQueueElement(tweet.date))

for t in tweets:
    print(t.time, t.queue_length, sep=",")

plt.plot_date(
    matplotlib.dates.date2num([t.time for t in tweets]),
    [t.queue_length for t in tweets],
    'b-'
)
plt.gcf().autofmt_xdate()
plt.savefig('plot.png')
