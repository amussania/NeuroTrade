import streamlit as st

KNOWLEDGE_BASE = {
    "🧠 Intelligence Score": {
        "question": "What is the Combined Intelligence Score?",
        "levels": [
            """The Combined Intelligence Score is a single number from 0 to 100 that tells you how bullish or bearish the market is for any asset right now.

0 to 30 means Strong Bear. The market is showing serious weakness.
31 to 45 means Weak Bear. More negative than positive signals.
46 to 55 means Neutral. Mixed signals with no clear direction.
56 to 70 means Weak Bull. More positive than negative signals.
71 to 100 means Strong Bull. The market is showing serious strength.

It combines four signals: Fear and Greed at 30%, 24 hour momentum at 25%, 7 day trend at 25%, and on-chain volume at 20%.

Did that make sense or would you like me to explain it differently?""",
            """Think of the Intelligence Score like a weather forecast but for crypto.

Instead of telling you if it will rain, it tells you if the market feels positive or negative right now.

A score of 75 is like a sunny forecast. A score of 20 is like a storm warning.

It looks at four things happening in the market right now and combines them into one number so you don't have to check everything yourself.

Is that clearer? Want me to explain what the four signals are?""",
            """Imagine you are trying to decide if you should go to a market to buy something.

You ask four friends for their opinion. One checks the news. One checks how busy the market was yesterday. One checks if prices have been going up or down this week. One checks how many people are actively trading.

The Intelligence Score does exactly that for crypto. It asks four different data sources for their view and combines them into one number.

If most of them say positive things, the score is high. If most say negative, the score is low. Simple as that.

Not financial advice."""
        ]
    },
    "😨 Fear & Greed": {
        "question": "What is the Fear and Greed Index?",
        "levels": [
            """The Fear and Greed Index measures the overall emotion of the crypto market on a scale from 0 to 100.

0 to 25 is Extreme Fear. People are panicking and selling.
26 to 45 is Fear. The market is nervous.
46 to 55 is Neutral. No strong emotion either way.
56 to 75 is Greed. People are excited and buying.
76 to 100 is Extreme Greed. People are rushing in without thinking.

The key insight is this: extreme fear has historically been a good time to look for buying opportunities. Extreme greed has historically preceded corrections.

The platform shows today's reading, the last 7 days, and a 30 day trend.

Did that make sense?""",
            """Think of the Fear and Greed Index like a crowd at a market.

When everyone is panicking and running away from the market that is extreme fear. Things are often on sale at that point.

When everyone is rushing in excitedly and prices are shooting up that is extreme greed. That is often when things are overpriced.

The smart approach is often the opposite of the crowd. Buy when others are fearful. Be careful when others are greedy.

Want me to explain how NeuroTrade uses this signal?""",
            """Imagine a fruit market. When it rains heavily nobody wants to go and the fruit seller drops prices to attract buyers. That is extreme fear in crypto.

When the sun is shining and everyone wants fruit the seller raises prices because people are happy to pay more. That is extreme greed in crypto.

The Index just measures how much it is raining or shining in the market right now.

Not financial advice."""
        ]
    },
    "⛓ On-Chain Data": {
        "question": "What is on-chain data?",
        "levels": [
            """On-chain data is information recorded directly on the Bitcoin blockchain. Unlike prices which can be influenced by speculation, on-chain data shows you what is actually happening on the network.

NeuroTrade tracks:
Hash Rate: How much computing power is securing Bitcoin. Higher means stronger network.
Daily Transactions: How many transfers happened today. More activity means more demand.
Block Time: How fast new blocks are being created. Closer to 10 minutes is ideal.
BTC Circulating: Total Bitcoin in existence out of 21 million maximum.
Trade Volume: How much BTC moved through exchanges today.
Network Health: Rated High Medium or Low based on transaction count.

Why does this matter? You can fake a price pump. You cannot fake real network activity.

Did that make sense?""",
            """Think of Bitcoin like a city. On-chain data is like the city's activity report.

How many cars are on the roads today. How busy the shops are. How much electricity the city is using.

If the city is bustling with activity that tells you it is healthy and growing. If it is empty that tells you something is wrong regardless of what the estate agents are saying about property prices.

On-chain data lets you look at what Bitcoin is actually doing rather than just what people are saying about it.

Want me to explain what each specific metric means?""",
            """Imagine you want to know if a restaurant is actually popular or just has good marketing.

You could look at their Instagram which they control. Or you could stand outside and count how many real customers walk in.

On-chain data is counting the real customers. It is the actual activity on the Bitcoin network that nobody can fake or manipulate.

Not financial advice."""
        ]
    },
    "🐋 Whale Activity": {
        "question": "What is whale activity?",
        "levels": [
            """Whales are wallets that hold very large amounts of Bitcoin, typically worth millions of dollars. When whales move their Bitcoin it can significantly impact the market.

NeuroTrade tracks unconfirmed Bitcoin transactions over 10 BTC in the mempool, which is the waiting room for transactions before they are confirmed on the blockchain.

For each whale transaction you can see:
The transaction hash as an identifier.
The BTC amount being moved.
Number of inputs and outputs.
Size rating of Standard Medium or Large.

Why does this matter? When whales move large amounts to exchanges it can signal selling pressure. When they move off exchanges it can signal long term holding.

Did that make sense?""",
            """Think of whales like the big supermarkets in a town. When a big supermarket decides to sell off a huge amount of stock it affects prices for everyone.

In crypto when someone moves 500 Bitcoin worth millions of dollars that is a significant event. It can push prices up or down depending on what they do with it.

NeuroTrade shows you these large movements as they are happening in real time before they are even confirmed.

Want me to explain what to look for in whale transactions?""",
            """Imagine you are at an auction. Most people are bidding small amounts. Then suddenly a very wealthy person walks in.

Everyone watches what that person does. If they start buying aggressively prices go up. If they start selling everyone gets nervous.

Whales are those wealthy people in the crypto market. Tracking their movements gives you information that most retail traders never look at.

Not financial advice."""
        ]
    },
    "🌍 Macro Intelligence": {
        "question": "How do interest rates and the dollar affect crypto?",
        "levels": [
            """Macro intelligence tracks four key economic indicators from the US Federal Reserve that historically influence crypto prices.

Fed Funds Rate: The interest rate banks charge each other. When rates are high money is expensive to borrow so investors move away from risky assets like crypto. When rates are low investors take more risk.

US Dollar Index: Measures how strong the dollar is. A strong dollar is historically bearish for crypto because crypto is priced in dollars. A weak dollar is historically bullish.

10 Year Inflation Expectations: What the market thinks inflation will be. High inflation can drive investors toward crypto as a hedge.

Unemployment Rate: Measures economic health. High unemployment often leads to economic uncertainty.

Did that make sense?""",
            """Think of it like this. When a bank offers you 5% interest on your savings account for zero risk, why would you put money into volatile crypto?

But when savings accounts offer almost nothing you start looking for better returns elsewhere. That is when crypto becomes more attractive.

The Federal Reserve controls these interest rates. When they raise rates crypto tends to struggle. When they cut rates crypto tends to benefit.

The dollar works similarly. When the dollar is strong everything priced in dollars including crypto gets relatively more expensive for global buyers.

Want me to explain what the current macro environment means for crypto?""",
            """Imagine the economy is a big water system. The Federal Reserve controls the tap.

When they tighten the tap less money flows and risky investments like crypto dry up.

When they open the tap money flows freely and some of it finds its way into crypto.

Macro intelligence just tells you how open or closed the tap is right now.

Not financial advice."""
        ]
    },
    "📈 Price Momentum": {
        "question": "What do price momentum and trend signals mean?",
        "levels": [
            """Price momentum measures how fast and in which direction an asset's price is moving.

NeuroTrade tracks two timeframes:
24 Hour Momentum: How much the price has moved in the last 24 hours. A big positive move signals short term strength. A big negative move signals short term weakness.
7 Day Trend: How much the price has moved over the last week. This filters out daily noise and shows the broader direction.

Both are mapped onto the 0 to 100 scale and fed into the Intelligence Score. Together they account for 50% of the total score.

A rising 7 day trend combined with positive 24 hour momentum is a strong bullish signal. A falling trend with negative momentum is a strong bearish signal.

Did that make sense?""",
            """Think of price momentum like a ball rolling down a hill.

Once it starts rolling it tends to keep going in the same direction. The 24 hour momentum tells you how fast the ball is moving right now. The 7 day trend tells you which direction the hill is sloping.

If the hill slopes upward and the ball is moving fast upward that is a strong positive signal. If the hill slopes down and the ball is accelerating downward that is a warning sign.

Want me to explain how this feeds into the Intelligence Score?""",
            """Imagine you are watching a train. The 24 hour momentum is how fast it is moving right now. The 7 day trend is which direction the tracks are pointing.

You want both pointing in the same direction before drawing any conclusions.

Not financial advice."""
        ]
    },
    "🎯 Signal Accuracy": {
        "question": "What is the Signal Accuracy Tracker?",
        "levels": [
            """The Signal Accuracy Tracker measures how often NeuroTrade's contrarian signals have been correct over the last 30 days.

It tracks two types of signals:
Fear Reversal Signals: When the Fear and Greed Index hits Extreme Fear below 30. Historically price goes up within 7 days.
Greed Reversal Signals: When the Fear and Greed Index hits Extreme Greed above 70. Historically price goes down within 7 days.

The tracker shows how many of these signals occurred and what percentage of the time the price moved in the predicted direction 7 days later.

Currently showing around 61 to 65 percent win rate. To put that in context Renaissance Technologies, the greatest trading firm in history, achieves around 66 percent. Anything above 55 percent is considered valuable.

Did that make sense?""",
            """Think of it like a weather forecaster's track record.

If a forecaster predicted rain 10 times and it rained 6 of those times they have a 60 percent accuracy rate. That is actually pretty good for complex systems.

NeuroTrade's Signal Accuracy Tracker does the same thing for market signals. It looks back at every time the Fear and Greed hit extreme levels and checks what happened to the price 7 days later.

A 61 to 65 percent accuracy rate means the signal is right more often than it is wrong. Over many decisions that adds up significantly.

Want me to explain what to do with this information?""",
            """Imagine you flip a coin. You win if it lands heads. 50% of the time you win.

Now imagine you have a special coin that lands heads 62% of the time. Over 100 flips that makes a massive difference even though each individual flip still feels uncertain.

That is what a 62% signal accuracy means. Not perfect. Not guaranteed. But meaningfully better than random.

Not financial advice."""
        ]
    },
    "📰 News Sentiment": {
        "question": "How does news sentiment work?",
        "levels": [
            """NeuroTrade pulls live headlines from thousands of news sources every 30 minutes and automatically classifies each one as Bullish, Bearish or Neutral.

Bullish keywords include: surge, rally, gain, high, bull, rise, record, adoption, approve.
Bearish keywords include: crash, drop, fall, bear, hack, ban, sell, fear, warning.

Why does this matter? Crypto markets are heavily sentiment driven. A single major news story can move prices by 10 to 20 percent within hours.

By seeing the overall tone of current news at a glance you can understand whether the narrative around crypto is positive or negative right now without reading dozens of articles.

Did that make sense?""",
            """Think of news sentiment like checking the mood of a crowd before you walk into a room.

If you hear laughing and excited chatter before you open the door you know the mood is positive. If you hear arguments and worried voices you know something is wrong.

NeuroTrade reads the headlines so you don't have to and tells you what the overall mood of crypto news is right now. Bullish means mostly good news. Bearish means mostly bad news.

Want me to explain how to use this alongside the other signals?""",
            """Imagine crypto Twitter is a giant conversation. News sentiment is like having someone stand in the middle of that conversation and tell you whether people sound excited or worried overall.

You don't need to read every tweet. You just need to know the general mood.

Not financial advice."""
        ]
    },
    "📊 Signal Intelligence": {
        "question": "What does the Signal Intelligence section show?",
        "levels": [
            """Signal Intelligence gives you a 30 day overview of market sentiment patterns. It shows four key stats:

Extreme Fear Days: How many of the last 30 days had a Fear and Greed score below 25. More extreme fear days historically means more buying opportunities were available.

30 Day Average Sentiment: The average Fear and Greed score over the last month. This tells you whether the overall climate has been fearful or greedy.

Sentiment Trend: Whether today's sentiment is better or worse than the 30 day average. Improving means the mood is getting more positive. Deteriorating means it is getting more negative.

Consecutive Days in Zone: How many days in a row the market has been in the current sentiment zone.

Did that make sense?""",
            """Think of Signal Intelligence like a monthly weather summary.

Instead of just knowing today's weather you can see how many stormy days there were this month, what the average temperature was, and whether it has been getting warmer or colder recently.

For crypto that means knowing whether the last 30 days have been mostly fearful or greedy, and whether things are improving or getting worse.

Want me to explain what patterns to look for?""",
            """Imagine you are checking if summer is coming.

You don't just look at today. You look at the last 30 days. How many cold days were there? Is it getting warmer overall? How many days in a row has it been above a certain temperature?

Signal Intelligence does the same for market mood.

Not financial advice."""
        ]
    },
    "⟠ ETH Gas Prices": {
        "question": "What are Ethereum gas prices?",
        "levels": [
            """Gas prices are fees paid to process transactions on the Ethereum network. They are measured in Gwei, which is a tiny fraction of one ETH.

NeuroTrade shows three speeds:
Safe: The cheapest option. Your transaction processes slower but costs least.
Standard: A balanced option. Reasonable speed at a reasonable cost.
Fast: The most expensive option. Your transaction processes almost immediately.

Why does this matter? High gas prices mean the Ethereum network is very busy. Lots of people are transacting. This signals high demand and network activity which is generally a positive indicator for ETH.

Low gas prices mean the network is quiet. Less activity happening.

Did that make sense?""",
            """Think of gas prices like toll roads at different times of day.

During rush hour everyone is on the road and the toll is higher because road space is scarce. During the middle of the night the toll is cheap because there is plenty of space.

High ETH gas prices mean rush hour on the Ethereum network. Lots of people are using it and paying a premium to get their transactions through quickly.

Want me to explain what high gas prices might mean for ETH's price?""",
            """Imagine a busy restaurant on a Saturday night. There is a queue to get in and you might pay more for a table.

That is high gas prices on Ethereum. The network is packed and people are paying extra to jump the queue.

When a restaurant is always full it usually means the food is good and business is booming.

Not financial advice."""
        ]
    },
    "🔥 Trending Status": {
        "question": "What does trending status mean?",
        "levels": [
            """Trending status shows whether the selected asset is currently in the top 7 most searched coins on CoinGecko, the world's largest crypto data platform.

When an asset is trending it means retail attention is rapidly increasing. More people are searching for it, reading about it, and potentially preparing to buy it.

This matters because retail attention often precedes price movements. When something starts trending on CoinGecko it frequently means a wave of new buyers is about to enter.

NeuroTrade checks this every hour and shows you whether the asset is trending right now and its exact rank if it is.

Did that make sense?""",
            """Think of trending status like watching what is popular on Netflix.

When a show starts trending it means lots of people are suddenly watching it. In crypto when a coin starts trending on CoinGecko it means lots of people are suddenly searching for it.

More attention often means more buyers coming. More buyers usually means upward price pressure.

Want me to explain how to use trending status alongside other signals?""",
            """Imagine you notice a long queue outside a shop you had never paid attention to before.

That queue tells you something interesting is happening inside even before you know what it is.

Trending status is that queue. Lots of people are suddenly interested in this asset. That is worth paying attention to.

Not financial advice."""
        ]
    },
    "🚀 How to use this": {
        "question": "How do I use NeuroTrade to make better decisions?",
        "levels": [
            """Here is the recommended way to use NeuroTrade:

Step 1: Check the Intelligence Score for your asset. This gives you the overall picture instantly.

Step 2: Look at the Signal Breakdown to see which signals are driving the score. Are they all aligned or are they conflicting?

Step 3: Check the Fear and Greed Index. Is the market in extreme territory?

Step 4: Read the Macro Intelligence section. Are interest rates and the dollar working for or against crypto right now?

Step 5: Scan the News Sentiment. Is the current news cycle positive or negative?

Step 6: Check Whale Activity. Are large holders moving their Bitcoin?

Step 7: Look at the Signal Accuracy Tracker to understand how reliable the current signals have been historically.

Use all of these together to form a complete picture. Never rely on one signal alone.

Did that make sense?""",
            """Think of NeuroTrade like a doctor's consultation.

A good doctor does not just check your temperature and make a diagnosis. They check your blood pressure, your history, your symptoms together.

NeuroTrade does the same for crypto. Each section is one vital sign. The Intelligence Score is the overall diagnosis. Use them together.

Want me to walk you through a specific scenario?""",
            """Imagine you are deciding whether to buy an umbrella.

You check the weather forecast. You look out the window. You check if your friends are carrying umbrellas. You look at whether the sky is dark.

No single signal is enough. But when all of them point the same way you can be more confident in your decision.

That is exactly how to use NeuroTrade.

Not financial advice."""
        ]
    }
}

def render_chatbot():
    st.markdown('<div class="section-header">NeuroTrade AI Guide</div>', unsafe_allow_html=True)

    st.markdown('''
    <div style="background:linear-gradient(135deg,rgba(0,212,255,0.06),rgba(124,58,237,0.06));
                border:1px solid rgba(0,212,255,0.15); border-radius:16px;
                padding:20px 24px; margin-bottom:20px;">
        <div style="color:#00D4FF; font-size:15px; font-weight:700; margin-bottom:6px;">
            🧠 Your Personal Crypto Intelligence Teacher
        </div>
        <div style="color:#64748B; font-size:13px; line-height:1.6;">
            Pick any topic below to learn what it means, how to read it, and why it matters.
            If the explanation is unclear just say so and I will explain it differently.
        </div>
    </div>
    ''', unsafe_allow_html=True)

    if 'chat_topic' not in st.session_state:
        st.session_state.chat_topic = None
    if 'chat_level' not in st.session_state:
        st.session_state.chat_level = 0
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    topics = list(KNOWLEDGE_BASE.keys())
    cols = st.columns(4)
    for i, topic in enumerate(topics):
        with cols[i % 4]:
            if st.button(topic, key=f"kb_{i}", use_container_width=True):
                st.session_state.chat_topic = topic
                st.session_state.chat_level = 0
                st.session_state.chat_history = []
                st.rerun()

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    if st.session_state.chat_topic:
        topic = st.session_state.chat_topic
        level = st.session_state.chat_level
        data = KNOWLEDGE_BASE[topic]
        explanation = data["levels"][level]

        if not st.session_state.chat_history:
            st.session_state.chat_history.append({"role": "bot", "text": explanation})

        for msg in st.session_state.chat_history:
            if msg["role"] == "bot":
                st.markdown(f'''
                <div style="background:#1E293B; border-radius:12px 12px 12px 4px;
                            padding:16px 20px; margin-bottom:12px;
                            color:#CBD5E1; font-size:13px; line-height:1.8;">
                    {msg["text"].replace(chr(10), "<br>")}
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div style="background:rgba(0,212,255,0.08); border:1px solid #334155;
                            border-radius:12px 12px 4px 12px;
                            padding:12px 20px; margin-bottom:12px;
                            color:#E2E8F0; font-size:13px; line-height:1.8;
                            margin-left:40px;">
                    {msg["text"]}
                </div>
                ''', unsafe_allow_html=True)

        btn_col1, btn_col2, btn_col3 = st.columns([2, 2, 1])

        with btn_col1:
            if level < len(data["levels"]) - 1:
                if st.button("Still confused, explain differently", key="simpler", use_container_width=True):
                    st.session_state.chat_level += 1
                    next_explanation = data["levels"][st.session_state.chat_level]
                    st.session_state.chat_history.append({"role": "user", "text": "Can you explain that differently?"})
                    st.session_state.chat_history.append({"role": "bot", "text": next_explanation})
                    st.rerun()
            else:
                st.markdown('<div style="color:#10B981; font-size:12px; padding:8px 0;">You have seen all explanation levels for this topic.</div>', unsafe_allow_html=True)

        with btn_col2:
            if st.button("I understand, next topic", key="next_topic", use_container_width=True):
                current_idx = topics.index(topic)
                next_idx = (current_idx + 1) % len(topics)
                st.session_state.chat_topic = topics[next_idx]
                st.session_state.chat_level = 0
                st.session_state.chat_history = []
                st.rerun()

        with btn_col3:
            if st.button("Reset", key="reset_chat", use_container_width=True):
                st.session_state.chat_topic = None
                st.session_state.chat_level = 0
                st.session_state.chat_history = []
                st.rerun()
    else:
        st.markdown('''
        <div style="text-align:center; padding:32px; color:#334155; font-size:13px;">
            Select a topic above to start learning
        </div>
        ''', unsafe_allow_html=True)
