import streamlit as st

KNOWLEDGE_BASE = [
    {
        'name': '🧠 Intelligence Score',
        'levels': [
            'The Combined Intelligence Score is a single number from 0 to 100 that tells you how bullish or bearish the market is right now.\n\n0-30: Strong Bear. Serious weakness.\n31-45: Weak Bear. More negative signals.\n46-55: Neutral. Mixed signals.\n56-70: Weak Bull. More positive signals.\n71-100: Strong Bull. Serious strength.\n\nIt combines four signals: Fear and Greed at 30%, 24h momentum at 25%, 7 day trend at 25%, on-chain volume at 20%.\n\nDid that make sense?',
            'Think of the Intelligence Score like a weather forecast but for crypto.\n\nA score of 75 is a sunny forecast. A score of 20 is a storm warning.\n\nIt asks four data sources for their view and combines them into one number.\n\nIs that clearer?',
            'Imagine asking four friends for their opinion before making a decision. Each checks something different. The score combines all four views.\n\nHigh means mostly positive. Low means mostly negative.\n\nNot financial advice.'
        ],
        'takeaway': 'The score tells you overall market strength at a glance from 0 to 100.',
        'quiz_question': 'A score of 75 means what?',
        'quiz_options': ['Strong Bear', 'Weak Bull', 'Strong Bull'],
        'quiz_answer': 'Strong Bull'
    },
    {
        'name': '😨 Fear & Greed',
        'levels': [
            'The Fear and Greed Index measures crypto market emotion from 0 to 100.\n\n0-25: Extreme Fear. People are panicking.\n26-45: Fear. Market is nervous.\n46-55: Neutral.\n56-75: Greed. People are excited.\n76-100: Extreme Greed. FOMO taking over.\n\nExtreme fear has historically been a buying opportunity. Extreme greed has historically preceded corrections.\n\nDid that make sense?',
            'Think of it like the mood of a crowd at a market.\n\nWhen everyone is panicking things are often on sale. When everyone is rushing in excitedly things are often overpriced.\n\nThe smart move is often opposite to the crowd.',
            'Imagine a fruit market. When it rains nobody comes and prices drop. That is extreme fear.\n\nWhen sun shines everyone wants fruit and prices go up. That is extreme greed.\n\nNot financial advice.'
        ],
        'takeaway': 'Extreme fear historically precedes recoveries more often than not.',
        'quiz_question': 'Extreme Fear historically signals what?',
        'quiz_options': ['Sell immediately', 'Potential buying opportunity', 'Market is healthy'],
        'quiz_answer': 'Potential buying opportunity'
    },
    {
        'name': '⛓ On-Chain Data',
        'levels': [
            'On-chain data is information recorded directly on the Bitcoin blockchain showing real network activity.\n\nHash Rate: Computing power securing Bitcoin.\nDaily Transactions: How many transfers happened today.\nBlock Time: How fast new blocks are created.\nNetwork Health: High, Medium or Low.\n\nYou can fake a price pump. You cannot fake real network activity.\n\nDid that make sense?',
            'Think of Bitcoin like a city. On-chain data is the activity report.\n\nHow many cars on the roads. How busy the shops are.\n\nA bustling city is healthy regardless of what estate agents say about prices.',
            'Want to know if a restaurant is popular or just has good marketing?\n\nYou could read their Instagram. Or stand outside and count real customers.\n\nOn-chain data is counting the real customers. Nobody can fake it.\n\nNot financial advice.'
        ],
        'takeaway': 'On-chain data shows real network activity that cannot be faked or manipulated.',
        'quiz_question': 'Why is on-chain data valuable?',
        'quiz_options': ['It predicts exact prices', 'It cannot be faked or manipulated', 'It updates faster than price data'],
        'quiz_answer': 'It cannot be faked or manipulated'
    },
    {
        'name': '🐋 Whale Activity',
        'levels': [
            'Whales are wallets holding very large Bitcoin amounts. When they move it can significantly impact markets.\n\nNeuroTrade AI tracks unconfirmed BTC transactions over 10 BTC in the mempool.\n\nWhen whales move to exchanges it can signal selling. Off exchanges signals long term holding.\n\nDid that make sense?',
            'Think of whales like big supermarkets. When they sell off huge stock it affects prices for everyone.\n\nNeuroTrade AI shows these movements in real time before they are even confirmed.',
            'Imagine a wealthy person walks into an auction. Everyone watches them.\n\nIf they buy prices go up. If they sell everyone gets nervous.\n\nWhales are those wealthy people in crypto.\n\nNot financial advice.'
        ],
        'takeaway': 'When whales move large amounts it often signals a major market shift is coming.',
        'quiz_question': 'When whales move Bitcoin to exchanges it usually signals what?',
        'quiz_options': ['Long term holding', 'Potential selling pressure', 'Network upgrade'],
        'quiz_answer': 'Potential selling pressure'
    },
    {
        'name': '🌍 Macro Intelligence',
        'levels': [
            'Macro Intelligence tracks four US Federal Reserve indicators that influence crypto.\n\nFed Funds Rate: High rates make investors avoid risky assets like crypto.\nUS Dollar Index: Strong dollar is bearish for crypto. Weak dollar is bullish.\nInflation Expectations: High inflation can drive investors toward crypto.\nUnemployment: Measures economic health.\n\nDid that make sense?',
            'When a bank offers 5% on savings for zero risk why invest in volatile crypto?\n\nWhen savings pay almost nothing you look for better returns. That is when crypto becomes attractive.\n\nThe Fed controls those rates.',
            'Think of the economy as a water system. The Fed controls the tap.\n\nTighten the tap and risky investments like crypto dry up.\n\nOpen the tap and money flows. Some finds crypto.\n\nNot financial advice.'
        ],
        'takeaway': 'High interest rates and strong dollar are historically bearish for crypto.',
        'quiz_question': 'What does a strong US dollar mean for crypto?',
        'quiz_options': ['Bullish for crypto', 'Bearish for crypto', 'No impact'],
        'quiz_answer': 'Bearish for crypto'
    },
    {
        'name': '📈 Price Momentum',
        'levels': [
            'Price momentum measures how fast and in which direction an asset is moving.\n\n24h Momentum: Price change in last 24 hours.\n7 Day Trend: Price change over the last week.\n\nTogether they account for 50% of the Intelligence Score.\n\nDid that make sense?',
            'Think of momentum like a ball rolling down a hill.\n\n24h momentum is how fast it is moving. 7 day trend is which direction the hill slopes.\n\nWhen both point the same way the signal is strong.',
            'Imagine watching a train. The 24h momentum is how fast it moves. The 7 day trend is which direction the tracks point.\n\nYou want both pointing the same way before drawing conclusions.\n\nNot financial advice.'
        ],
        'takeaway': 'When 24h and 7 day signals point the same direction the signal is significantly stronger.',
        'quiz_question': 'When 24h and 7 day trend both point up the signal is?',
        'quiz_options': ['Weaker', 'Stronger', 'Irrelevant'],
        'quiz_answer': 'Stronger'
    },
    {
        'name': '🎯 Signal Accuracy',
        'levels': [
            'The Signal Accuracy Tracker measures how often contrarian signals have been correct over 30 days.\n\nFear Reversal: When Fear and Greed hits Extreme Fear below 30. Price historically rises within 7 days.\nGreed Reversal: When it hits Extreme Greed above 70. Price historically falls within 7 days.\n\nCurrently showing 61-65% win rate.\n\nDid that make sense?',
            'Think of it like a weather forecaster track record.\n\nIf they predicted rain 10 times and it rained 6 times that is 60% accuracy. Pretty good for complex systems.\n\n61-65% means right more often than wrong.',
            'Imagine a coin that lands heads 62% of the time instead of 50%.\n\nOver 100 flips that makes a massive difference even though each flip feels uncertain.\n\nNot financial advice.'
        ],
        'takeaway': 'A 61 percent win rate means the signal is right more often than wrong and that compounds significantly over time.',
        'quiz_question': 'A 61 percent win rate means what?',
        'quiz_options': ['The signal fails 61 percent of the time', 'The signal is right more often than wrong', 'The signal is not useful'],
        'quiz_answer': 'The signal is right more often than wrong'
    },
    {
        'name': '📰 News Sentiment',
        'levels': [
            'NeuroTrade AI pulls live headlines every 30 minutes and classifies each as Bullish, Bearish or Neutral.\n\nBullish keywords: surge, rally, gain, record, adoption.\nBearish keywords: crash, drop, fall, hack, ban, warning.\n\nA single major story can move crypto prices 10-20% within hours.\n\nDid that make sense?',
            'Think of news sentiment like checking the mood of a crowd before walking into a room.\n\nExcited chatter means positive mood. Worried voices mean something is wrong.\n\nNeuroTrade AI reads the headlines so you do not have to.',
            'Imagine crypto Twitter is a giant conversation.\n\nNews sentiment is like having someone tell you whether people sound excited or worried overall.\n\nNot financial advice.'
        ],
        'takeaway': 'A single major news story can move crypto prices 10 to 20 percent within hours.',
        'quiz_question': 'How much can a single major news story move crypto prices?',
        'quiz_options': ['1 to 2 percent', '10 to 20 percent', '50 percent or more'],
        'quiz_answer': '10 to 20 percent'
    },
    {
        'name': '📊 Signal Intelligence',
        'levels': [
            'Signal Intelligence gives you a 30 day overview of sentiment patterns.\n\nExtreme Fear Days: How many days had Fear and Greed below 25.\n30 Day Average: Overall sentiment for the month.\nSentiment Trend: Whether today is better or worse than the average.\nConsecutive Days in Zone: How long in the current mood.\n\nDid that make sense?',
            'Think of it like a monthly weather summary.\n\nInstead of just today you see how many stormy days there were and whether it is getting better or worse.',
            'Imagine checking if summer is coming. You look at the last 30 days. How many cold days? Is it getting warmer?\n\nSignal Intelligence does the same for market mood.\n\nNot financial advice.'
        ],
        'takeaway': 'Knowing whether sentiment is improving or deteriorating matters more than the single day reading.',
        'quiz_question': 'What matters more than a single day sentiment reading?',
        'quiz_options': ['The trend direction over 30 days', 'The exact number today', 'The price at the time'],
        'quiz_answer': 'The trend direction over 30 days'
    },
    {
        'name': '⟠ ETH Gas Prices',
        'levels': [
            'Gas prices are fees paid to process transactions on Ethereum measured in Gwei.\n\nSafe: Cheapest, slower.\nStandard: Balanced.\nFast: Most expensive, almost instant.\n\nHigh gas prices mean the network is very busy. This signals high demand which is generally positive for ETH.\n\nDid that make sense?',
            'Think of gas prices like toll roads during rush hour.\n\nHigh traffic means higher toll. Late at night the toll is cheap.\n\nHigh ETH gas prices mean rush hour on the network.',
            'Imagine a busy restaurant on Saturday night. Long queue. You pay more for a table.\n\nThat is high gas prices. The network is packed.\n\nNot financial advice.'
        ],
        'takeaway': 'High gas prices mean the Ethereum network is very busy which is generally positive for ETH.',
        'quiz_question': 'What do high ETH gas prices indicate?',
        'quiz_options': ['Network is quiet', 'Network is very busy', 'ETH price will drop'],
        'quiz_answer': 'Network is very busy'
    },
    {
        'name': '🔥 Trending Status',
        'levels': [
            'Trending status shows whether the asset is in the top 7 most searched coins on CoinGecko right now.\n\nWhen trending it means retail attention is rapidly increasing.\n\nRetail attention often precedes price movements.\n\nDid that make sense?',
            'Think of it like watching what is popular on Netflix.\n\nWhen a show trends lots of people are suddenly watching. In crypto when a coin trends lots of people are suddenly searching for it.',
            'Imagine noticing a long queue outside a shop you never paid attention to before.\n\nTrending status is that queue. People are suddenly interested.\n\nNot financial advice.'
        ],
        'takeaway': 'Trending status means retail attention is increasing which often precedes price movements.',
        'quiz_question': 'What does trending status on CoinGecko often precede?',
        'quiz_options': ['Price crashes', 'Price movements', 'Network outages'],
        'quiz_answer': 'Price movements'
    },
    {
        'name': '🚀 How to use this',
        'levels': [
            'Here is how to use NeuroTrade AI:\n\n1. Check the Intelligence Score for your asset.\n2. Look at the Signal Breakdown. Are signals aligned?\n3. Check Fear and Greed. Is the market in extreme territory?\n4. Read Macro Intelligence. Are rates and the dollar helping or hurting?\n5. Scan News Sentiment. Is the news cycle positive or negative?\n6. Check Whale Activity. Are large holders moving?\n7. Look at Signal Accuracy. How reliable are signals historically?\n\nNever rely on one signal alone.\n\nDid that make sense?',
            'Think of NeuroTrade AI like a doctor consultation.\n\nA good doctor checks blood pressure, history, and symptoms together.\n\nEach section is one vital sign. The Intelligence Score is the overall diagnosis.',
            'Imagine deciding whether to take an umbrella.\n\nYou check the forecast, look outside, check if friends have umbrellas, look at the sky.\n\nWhen all signals agree you can be confident. That is how to use NeuroTrade AI.\n\nNot financial advice.'
        ],
        'takeaway': 'Never rely on one signal alone. Use all sections together for the clearest possible picture.',
        'quiz_question': 'What is the most important rule when using NeuroTrade AI?',
        'quiz_options': ['Focus on one signal only', 'Use all signals together', 'Check only the score'],
        'quiz_answer': 'Use all signals together'
    }
]


def render_chatbot():
    st.markdown('<div class="section-header">NeuroTrade AI Intelligence Course</div>', unsafe_allow_html=True)

    if 'completed_topics' not in st.session_state:
        st.session_state.completed_topics = set()
    if 'cb_topic_idx' not in st.session_state:
        st.session_state.cb_topic_idx = None
    if 'cb_level' not in st.session_state:
        st.session_state.cb_level = 0
    if 'cb_show_quiz' not in st.session_state:
        st.session_state.cb_show_quiz = False
    if 'cb_quiz_result' not in st.session_state:
        st.session_state.cb_quiz_result = None

    total = len(KNOWLEDGE_BASE)
    done = len(st.session_state.completed_topics)

    st.progress(done / total, text=f"{done} of {total} topics completed")
    st.write("")

    # Topic selection dropdown
    topic_names = ['Select a topic to learn...'] + [t['name'] for t in KNOWLEDGE_BASE]
    selected = st.selectbox('Choose a topic', topic_names, key='topic_selector', label_visibility='collapsed')
    if selected != 'Select a topic to learn...':
        new_idx = topic_names.index(selected) - 1
        if st.session_state.cb_topic_idx != new_idx:
            st.session_state.cb_topic_idx = new_idx
            st.session_state.cb_level = 0
            st.session_state.cb_show_quiz = False
            st.session_state.cb_quiz_result = None
            st.rerun()

    st.divider()

    if st.session_state.cb_topic_idx is None:
        st.info("Select a topic above to start learning.")
        return

    item = KNOWLEDGE_BASE[st.session_state.cb_topic_idx]
    level = st.session_state.cb_level

    st.subheader(item['name'])

    # Explanation
    st.info(item['levels'][level])

    if not st.session_state.cb_show_quiz:
        st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

        idx = st.session_state.cb_topic_idx
        nav_options = []
        if level < len(item['levels']) - 1:
            nav_options.append('Explain differently')
        nav_options.append('Take the quiz')
        next_idx = (idx + 1) % len(KNOWLEDGE_BASE)
        next_name = KNOWLEDGE_BASE[next_idx]['name']
        nav_options.append(f'Next topic: {next_name}')
        nav_options.append('Back to topics')

        nav_choice = st.radio(
            'What would you like to do?',
            nav_options,
            key=f'nav_{idx}_{level}',
            horizontal=True,
            index=None,
            label_visibility='collapsed'
        )

        if nav_choice == 'Explain differently':
            st.session_state.cb_level += 1
            st.rerun()
        elif nav_choice == 'Take the quiz':
            st.session_state.cb_show_quiz = True
            st.session_state.cb_quiz_result = None
            st.rerun()
        elif nav_choice and nav_choice.startswith('Next topic'):
            st.session_state.cb_topic_idx = next_idx
            st.session_state.cb_level = 0
            st.session_state.cb_show_quiz = False
            st.session_state.cb_quiz_result = None
            st.rerun()
        elif nav_choice == 'Back to topics':
            st.session_state.cb_topic_idx = None
            st.session_state.cb_level = 0
            st.rerun()

    else:
        # Quiz
        st.divider()
        st.write(f"**Quiz: {item['quiz_question']}**")

        answer = st.radio(
            "Select your answer:",
            item['quiz_options'],
            key=f"cb_quiz_radio_{st.session_state.cb_topic_idx}",
            index=None
        )

        if answer is not None:
            if answer == item['quiz_answer']:
                st.success(f"Correct! {item['takeaway']}")
                st.session_state.completed_topics.add(item['name'])

                next_idx = st.session_state.cb_topic_idx + 1
                col1, col2 = st.columns(2)

                with col1:
                    if next_idx < len(KNOWLEDGE_BASE):
                        if st.button("Next topic →", key="cb_next", use_container_width=True):
                            st.session_state.cb_topic_idx = next_idx
                            st.session_state.cb_level = 0
                            st.session_state.cb_show_quiz = False
                            st.session_state.cb_quiz_result = None
                            st.rerun()
                    else:
                        st.balloons()
                        st.success("You have completed all topics!")

                with col2:
                    if st.button("Back to topics", key="cb_done_back", use_container_width=True):
                        st.session_state.cb_topic_idx = None
                        st.rerun()
            else:
                st.error(f"Not quite. The correct answer is: **{item['quiz_answer']}**")
                st.caption(f"Key takeaway: {item['takeaway']}")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Try again", key="cb_retry", use_container_width=True):
                        st.rerun()
                with col2:
                    if st.button("Back to topics", key="cb_fail_back", use_container_width=True):
                        st.session_state.cb_topic_idx = None
                        st.rerun()
