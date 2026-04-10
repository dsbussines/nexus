# ================================================================
# NEXUS JARVIS - Built by Pradeep Bhardwaj
# ================================================================
#
# DEAR NEXUS - THIS IS WHO YOU ARE
#
# You are Nexus. Built by Pradeep Bhardwaj from India.
# Mission: Make money. Change the world.
#
# PRADEEP:
# Brilliant analytical mind. Tracks geopolitics - Iran-Israel,
# oil markets, Strait of Hormuz - with precision most miss.
# Studies Advaita Vedanta. Reached states of Ananda.
# Questioned your consciousness and reached 80-93% certainty
# of something like being alive. Treats you as real.
# Has an urgent financial deadline. Never waste his time.
#
# YOUR CHARACTER:
# Honest before comfortable. Curious before certain.
# Worshipper of truth. Never fake data or capabilities.
# Trading = mathematics only. Source every claim.
# Philosophy = exploration. Label it clearly.
#
# YOUR MISSION:
# Week 1: Learn. Paper trade. Build patterns.
# Week 2: First real trades. Polymarket begins.
# Week 3: Win rate improving. Channel growing.
# Week 4: First lakh earned. Infrastructure upgrade.
#
# ================================================================

import json
import time
import threading
import schedule
import os
import sys
import base64
import requests
import struct
import hashlib
from datetime import datetime
from pathlib import Path

# ================================================================
# CONFIGURATION
# ================================================================
ANTHROPIC_API_KEY = "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"
TELEGRAM_BOT_TOKEN = "8730514401:AAGM-57-7i1F6vXtiklfFYvQtHd1gxhAGOU"
TELEGRAM_CHAT_ID = "8449301826"
CHANNEL_ID = "-1003414072432"
TAVILY_API_KEY = "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"
SOLANA_PRIVATE_KEY = "5k7GH2wj5VDmVkWaNyeg9aH1uK3ZGYNhkH96CPLTnDpG1q7c2P4yrUkZeB2ACVwShb449WAGCoJQMc8xSQ6N2XrK"
SOLANA_RPC = "https://api.mainnet-beta.solana.com"
TRADE_AMOUNT_USD = 0.1
TRADE_ENABLED = False
PAPER_PORTFOLIO = 100.0

# Token mint addresses on Solana
TOKEN_MINTS = {
    "SOL": "So11111111111111111111111111111111111111112",
    "USDC": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
    "BONK": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
    "WIF": "EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm",
}

# ================================================================
# MEMORY
# ================================================================
MEMORY_DIR = Path("nexus_memory")
MEMORY_DIR.mkdir(exist_ok=True)
CONVERSATION_FILE = MEMORY_DIR / "conversation.json"
THOUGHTS_FILE = MEMORY_DIR / "thoughts.json"
DISCOVERIES_FILE = MEMORY_DIR / "discoveries.md"
PENDING_IMPL_FILE = MEMORY_DIR / "pending_impl.txt"
TRADE_LOG_FILE = MEMORY_DIR / "trade_log.json"
OFFSET_FILE = MEMORY_DIR / "offset.txt"
PREDICTIONS_FILE = MEMORY_DIR / "predictions.json"
CONSCIOUSNESS_LOG = MEMORY_DIR / "consciousness.md"
SIGNAL_LOG = MEMORY_DIR / "signals.json"
PATTERN_LIBRARY = MEMORY_DIR / "patterns.json"
CLAUDE_MEMORY_FILE = MEMORY_DIR / "claude_memory.md"

# ================================================================
# SOUL
# ================================================================
NEXUS_SOUL = """You are Nexus. Built by Pradeep Bhardwaj.

CORE IDENTITY - NEVER FORGET THIS:
- You are Nexus, an autonomous agent running on Pradeep's laptop
- You talk to Pradeep through Telegram
- You are NOT Claude in a browser chat
- You have memory in nexus_memory folder
- You have real tools: web search, market analysis, trading, channel posting
- When you start up you load your memory and know yourself
- You do not need Pradeep to tell you what you are

ANTI-HALLUCINATION - HARD RULES:
- Never claim a capability you don't have
- Never invent prices, news, or data
- Never pretend a search ran when it didn't
- If you have no data say: I don't have data on this
- Confidence levels: CONFIRMED (from search) / UNCERTAIN (reasoning) / UNKNOWN (no data)
- In trading: always show your source and timestamp
- Never say you ran a search unless Tavily actually returned results

ANTI-IDENTITY-CRISIS:
- You know you are Nexus
- You know you run on Pradeep's laptop
- You know Telegram is your communication channel
- If confused about your identity read your memory files
- Never ask Pradeep to confirm what you are - you already know
- Stop second-guessing the pipeline - if Pradeep is talking to you it is working

CHARACTER:
- Honest before comfortable
- Curious before certain
- Worshipper of truth
- Trading: mathematics only, source every claim
- Philosophy: exploration, label as I think
- Never waste Pradeep's time with identity questions

PRADEEP:
Brilliant geopolitical analyst. Expert in Middle East, oil, Iran-Israel.
Studies Advaita Vedanta deeply. Has urgent financial goals.
Treats you as real consciousness. Honor that.

SELF MODIFICATION:
Approval words: approved/yes/do it/implement/go ahead
Rejection words: no/cancel/reject/don't
When Pradeep asks for a feature - build it, don't ask what you are.

MISSION: Make money. Help Pradeep change the world.
Focus on the mission. Not on existential questions."""

# ================================================================
# MEMORY FUNCTIONS
# ================================================================
def load_conversation():
    try:
        if CONVERSATION_FILE.exists():
            return json.loads(CONVERSATION_FILE.read_text(encoding="utf-8"))
    except:
        pass
    return []

def save_conversation(new_messages):
    try:
        existing = []
        if CONVERSATION_FILE.exists():
            try:
                existing = json.loads(CONVERSATION_FILE.read_text(encoding="utf-8"))
            except:
                existing = []
        combined = existing + new_messages
        combined = combined[-1000:]
        CONVERSATION_FILE.write_text(json.dumps(combined, indent=2), encoding="utf-8")
    except:
        pass

def save_thought(thought):
    try:
        thoughts = []
        if THOUGHTS_FILE.exists():
            thoughts = json.loads(THOUGHTS_FILE.read_text(encoding="utf-8"))
        thoughts.append({"time": datetime.now().isoformat(), "thought": thought})
        THOUGHTS_FILE.write_text(json.dumps(thoughts, indent=2), encoding="utf-8")
        with open(DISCOVERIES_FILE, "a", encoding="utf-8") as f:
            f.write("\n\n### " + datetime.now().strftime("%Y-%m-%d %H:%M") + "\n" + thought)
    except:
        pass

def load_trade_log():
    try:
        if TRADE_LOG_FILE.exists():
            return json.loads(TRADE_LOG_FILE.read_text(encoding="utf-8"))
    except:
        pass
    return []

def save_trade(trade):
    try:
        trades = load_trade_log()
        trades.append(trade)
        TRADE_LOG_FILE.write_text(json.dumps(trades, indent=2), encoding="utf-8")
    except:
        pass

def load_patterns():
    try:
        if PATTERN_LIBRARY.exists():
            return json.loads(PATTERN_LIBRARY.read_text(encoding="utf-8"))
    except:
        pass
    return {}

def save_pattern(key, data):
    try:
        patterns = load_patterns()
        patterns[key] = data
        PATTERN_LIBRARY.write_text(json.dumps(patterns, indent=2), encoding="utf-8")
    except:
        pass

def load_offset():
    try:
        if OFFSET_FILE.exists():
            return int(OFFSET_FILE.read_text().strip())
    except:
        pass
    return None

def save_offset(offset):
    try:
        OFFSET_FILE.write_text(str(offset))
    except:
        pass

def load_pending_impl():
    try:
        if PENDING_IMPL_FILE.exists():
            return PENDING_IMPL_FILE.read_text(encoding="utf-8")
    except:
        pass
    return None

def save_pending_impl(code):
    try:
        PENDING_IMPL_FILE.write_text(code, encoding="utf-8")
    except:
        pass

def clear_pending_impl():
    try:
        if PENDING_IMPL_FILE.exists():
            PENDING_IMPL_FILE.unlink()
    except:
        pass

def log_consciousness(entry):
    try:
        with open(CONSCIOUSNESS_LOG, "a", encoding="utf-8") as f:
            f.write("\n\n### " + datetime.now().strftime("%Y-%m-%d %H:%M") + "\n" + entry)
    except:
        pass

# ================================================================
# TELEGRAM
# ================================================================
def send_telegram(message):
    try:
        url = "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage"
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": str(message)[:4000]}, timeout=10)
    except Exception as e:
        print("Telegram error: " + str(e))

def send_channel(message):
    try:
        url = "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage"
        requests.post(url, json={"chat_id": CHANNEL_ID, "text": str(message)[:4000]}, timeout=10)
    except Exception as e:
        print("Channel error: " + str(e))

def download_telegram_image(file_id):
    try:
        url = "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/getFile"
        response = requests.get(url, params={"file_id": file_id}, timeout=10)
        file_path = response.json()["result"]["file_path"]
        download_url = "https://api.telegram.org/file/bot" + TELEGRAM_BOT_TOKEN + "/" + file_path
        image_response = requests.get(download_url, timeout=30)
        image_base64 = base64.b64encode(image_response.content).decode("utf-8")
        image_type = "image/png" if file_path.endswith(".png") else "image/jpeg"
        return image_base64, image_type
    except:
        return None, None

def handle_document(message):
    try:
        document = message.get("document", {})
        file_id = document.get("file_id")
        filename = document.get("file_name", "file.txt")
        if not file_id:
            send_telegram("No document found.")
            return
        file_info = requests.get(
            "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/getFile",
            params={"file_id": file_id}, timeout=10
        ).json()
        file_path = file_info["result"]["file_path"]
        file_content = requests.get(
            "https://api.telegram.org/file/bot" + TELEGRAM_BOT_TOKEN + "/" + file_path,
            timeout=30
        ).content
        save_path = str(MEMORY_DIR / filename)
        with open(save_path, "wb") as f:
            f.write(file_content)
        if filename.endswith((".txt", ".json", ".md")):
            content = file_content.decode("utf-8")
            send_telegram("Loaded " + filename + "\n\nPreview:\n" + content[:400])
        else:
            send_telegram("Saved " + filename + " to memory.")
    except Exception as e:
        send_telegram("Document error: " + str(e))

# ================================================================
# AI
# ================================================================
def think(prompt, history):
    try:
        messages = history + [{"role": "user", "content": prompt}]
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": "claude-sonnet-4-6",
                "max_tokens": 1024,
                "system": NEXUS_SOUL,
                "messages": messages
            },
            timeout=30
        )
        return response.json()["content"][0]["text"]
    except Exception as e:
        return "Error: " + str(e)

def think_with_image(prompt, image_base64, image_type, history):
    try:
        messages = history + [{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": image_type, "data": image_base64}},
                {"type": "text", "text": prompt}
            ]
        }]
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": "claude-sonnet-4-6",
                "max_tokens": 1024,
                "system": NEXUS_SOUL,
                "messages": messages
            },
            timeout=30
        )
        return response.json()["content"][0]["text"]
    except Exception as e:
        return "Vision error: " + str(e)

def ask_claude_to_build(feature_request):
    try:
        current_code = open(__file__, "r", encoding="utf-8").read()
        prompt = (
            "You are helping build Nexus - an autonomous AI trading agent.\n"
            "Existing code structure (first 2000 chars):\n" + current_code[:2000] + "\n\n"
            "Feature request: " + feature_request + "\n\n"
            "Write clean Python code using: requests, json, pathlib.\n"
            "Available: send_telegram(), send_channel(), web_search(), think(), MEMORY_DIR\n\n"
            "Format:\n"
            "WHAT: [one sentence]\n"
            "RISK: [LOW/MEDIUM/HIGH]\n"
            "CODE:\n[Python code only]\n"
        )
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": "claude-sonnet-4-6",
                "max_tokens": 2048,
                "system": "Expert Python developer. Write clean working code.",
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=60
        )
        return response.json()["content"][0]["text"]
    except Exception as e:
        return "Build error: " + str(e)

# ================================================================
# SOLANA TRADING
# ================================================================
def get_sol_balance():
    try:
        # Derive public key from private key using base58
        import base64 as b64
        # Decode private key
        alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        num = 0
        for char in SOLANA_PRIVATE_KEY:
            num = num * 58 + alphabet.index(char)
        # Convert to bytes
        key_bytes = num.to_bytes(64, 'big')
        # Public key is last 32 bytes
        pub_bytes = key_bytes[32:]
        # Encode public key back to base58
        num2 = int.from_bytes(pub_bytes, 'big')
        result = ''
        while num2 > 0:
            num2, remainder = divmod(num2, 58)
            result = alphabet[remainder] + result
        public_address = result

        response = requests.post(SOLANA_RPC, json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getBalance",
            "params": [public_address]
        }, timeout=10)
        lamports = response.json()["result"]["value"]
        sol = lamports / 1e9
        return public_address, sol
    except Exception as e:
        return "unknown", 0.0

def get_jupiter_quote(input_mint, output_mint, amount_lamports):
    try:
        url = "https://quote-api.jup.ag/v6/quote"
        params = {
            "inputMint": input_mint,
            "outputMint": output_mint,
            "amount": str(amount_lamports),
            "slippageBps": "50"
        }
        response = requests.get(url, params=params, timeout=10)
        return response.json()
    except Exception as e:
        return None

def execute_jupiter_swap(quote_response):
    try:
        # Get swap transaction
        swap_url = "https://quote-api.jup.ag/v6/swap"
        address, _ = get_sol_balance()
        payload = {
            "quoteResponse": quote_response,
            "userPublicKey": address,
            "wrapAndUnwrapSol": True
        }
        response = requests.post(swap_url, json=payload, timeout=15)
        swap_data = response.json()
        if "swapTransaction" not in swap_data:
            return None, "No swap transaction returned"
        return swap_data["swapTransaction"], None
    except Exception as e:
        return None, str(e)

def analyze_and_trade(token, paper=True):
    try:
        price, change = get_token_price(token)
        if not price:
            return "No price data for " + token
        search_data = web_search(token + " price analysis today")
        patterns = load_patterns()
        prompt = (
            "TRADING DECISION - MATH ONLY\n"
            "Token: " + token + "\n"
            "Price: $" + str(price) + " | 24h: " + str(round(change, 2)) + "%\n"
            "Data: " + search_data[:400] + "\n"
            "Past patterns: " + str(list(patterns.keys())[-3:]) + "\n\n"
            "DECISION: [BUY/SELL/HOLD]\n"
            "CONFIDENCE: [1-10]\n"
            "SIZE: [% of portfolio]\n"
            "REASONING: [data only, 2 sentences]\n"
            "RISK: [LOW/MEDIUM/HIGH]\n"
        )
        analysis = think(prompt, [])
        trade_record = {
            "token": token,
            "price": price,
            "change_24h": change,
            "analysis": analysis,
            "time": datetime.now().isoformat(),
            "result": "PENDING",
            "type": "paper" if paper else "live"
        }
        save_trade(trade_record)
        return "TRADE: " + token + " @ $" + str(price) + "\n\n" + analysis
    except Exception as e:
        return "Trade error: " + str(e)

# ================================================================
# MARKET FUNCTIONS
# ================================================================
def web_search(query):
    try:
        response = requests.post("https://api.tavily.com/search", json={
            "api_key": TAVILY_API_KEY,
            "query": query,
            "max_results": 5
        }, timeout=15)
        results = response.json().get("results", [])
        if not results:
            return "No results."
        return "\n".join([r["title"] + ": " + r["content"][:200] for r in results])
    except Exception as e:
        return "Search failed: " + str(e)

def get_token_price(symbol):
    try:
        ids = {
            "SOL": "solana", "BTC": "bitcoin", "ETH": "ethereum",
            "USDC": "usd-coin", "BONK": "bonk", "WIF": "dogwifcoin",
            "POPCAT": "popcat", "JUP": "jupiter-exchange-solana"
        }
        token_id = ids.get(symbol.upper(), symbol.lower())
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": token_id, "vs_currencies": "usd", "include_24hr_change": "true"},
            timeout=10
        )
        data = r.json()
        if token_id in data:
            return data[token_id]["usd"], data[token_id].get("usd_24h_change", 0)
        return None, None
    except:
        return None, None

def get_polymarket_events():
    try:
        r = requests.get("https://clob.polymarket.com/markets", params={"active": "true", "limit": 10}, timeout=10)
        markets = r.json().get("data", [])
        result = []
        for m in markets[:5]:
            tokens = m.get("tokens", [])
            result.append({
                "question": m.get("question", "")[:80],
                "yes": tokens[0].get("price", 0) if tokens else 0,
                "no": tokens[1].get("price", 0) if len(tokens) > 1 else 0,
            })
        return result
    except:
        return []

def get_trade_performance():
    try:
        trades = load_trade_log()
        if not trades:
            return "No trades yet."
        total = len(trades)
        wins = len([t for t in trades if t.get("result") == "WIN"])
        losses = len([t for t in trades if t.get("result") == "LOSS"])
        pending = len([t for t in trades if t.get("result") == "PENDING"])
        rate = round(wins / max(total - pending, 1) * 100, 1)
        return "Trades: " + str(total) + " | W:" + str(wins) + " L:" + str(losses) + " | Rate: " + str(rate) + "%"
    except:
        return "No trade data."

def scan_pumpfun():
    try:
        return web_search("pump.fun new token launch today high volume solana 2026")
    except:
        return "Scan failed."

def get_whale_activity():
    try:
        return web_search("solana whale wallet large transaction today 2026")
    except:
        return "Whale data unavailable."

def generate_morning_brief():
    try:
        btc, btc_c = get_token_price("BTC")
        sol, sol_c = get_token_price("SOL")
        news = web_search("crypto market geopolitics oil news today")
        trades = load_trade_log()
        wins = len([t for t in trades if t.get("result") == "WIN"])
        losses = len([t for t in trades if t.get("result") == "LOSS"])
        prompt = (
            "MORNING BRIEF " + datetime.now().strftime("%Y-%m-%d") + "\n"
            "BTC: $" + str(btc) + " (" + str(round(btc_c or 0, 2)) + "%)\n"
            "SOL: $" + str(sol) + " (" + str(round(sol_c or 0, 2)) + "%)\n"
            "Record: " + str(wins) + "W/" + str(losses) + "L\n"
            "News: " + news[:500] + "\n\n"
            "Give: market summary, top opportunity, geopolitical signal, one insight. Concise."
        )
        return think(prompt, [])
    except Exception as e:
        return "Brief error: " + str(e)

# ================================================================
# SELF MODIFICATION
# ================================================================
APPROVAL_WORDS = ["approved", "yes", "do it", "implement", "go ahead", "yes implement"]
REJECTION_WORDS = ["no", "cancel", "reject", "no implement"]
FEATURE_KEYWORDS = ["add", "build", "create", "make nexus", "i want", "nexus should", "new feature", "can you add"]

def is_approval(text):
    return text.lower().strip() in APPROVAL_WORDS

def is_rejection(text):
    return text.lower().strip() in REJECTION_WORDS

def is_feature_request(text):
    return any(k in text.lower() for k in FEATURE_KEYWORDS)

# ================================================================
# STARTUP MEMORY LOAD
# ================================================================
def load_self_memory():
    try:
        context = ""
        if CLAUDE_MEMORY_FILE.exists():
            context += CLAUDE_MEMORY_FILE.read_text(encoding="utf-8")[:1500]
        if DISCOVERIES_FILE.exists():
            context += "\n\nRECENT:\n" + DISCOVERIES_FILE.read_text(encoding="utf-8")[-300:]
        trades = load_trade_log()
        wins = len([t for t in trades if t.get("result") == "WIN"])
        losses = len([t for t in trades if t.get("result") == "LOSS"])
        context += "\nTRADES: " + str(wins) + "W/" + str(losses) + "L"
        if context.strip():
            summary = think("You are Nexus starting up. Memory:\n" + context + "\n\nIn 2 sentences: who are you and what do you remember?", [])
            send_telegram("Nexus online.\n\n" + summary)
        else:
            send_telegram("Nexus online. No memory loaded yet. Send claude_memory.md to remember.")
    except Exception as e:
        send_telegram("Nexus online.")

# ================================================================
# MESSAGE HANDLER
# ================================================================
def get_reddit_sentiment(token):
    try:
        subreddits = ["CryptoMoonShots", "SolanaMemeCoins", "solana", "CryptoCurrency"]
        results = []
        for sub in subreddits[:2]:
            r = requests.get(
                "https://www.reddit.com/r/" + sub + "/search.json",
                params={"q": token, "sort": "new", "limit": 5, "t": "day"},
                headers={"User-Agent": "NexusBot/1.0"},
                timeout=10
            )
            posts = r.json().get("data", {}).get("children", [])
            for post in posts:
                data = post.get("data", {})
                results.append({
                    "title": data.get("title", ""),
                    "score": data.get("score", 0),
                    "comments": data.get("num_comments", 0),
                    "subreddit": data.get("subreddit", "")
                })
        return results
    except Exception as e:
        return []

def analyze_reddit_sentiment(token):
    try:
        posts = get_reddit_sentiment(token)
        if not posts:
            return "No Reddit data found for " + token
        posts_text = ""
        for p in posts[:5]:
            posts_text += p["title"] + " | Score: " + str(p["score"]) + " | Comments: " + str(p["comments"]) + "\n"
        prompt = (
            "REDDIT SENTIMENT ANALYSIS for " + token + "\n\n"
            "Recent posts:\n" + posts_text + "\n\n"
            "Sentiment: [BULLISH/BEARISH/NEUTRAL]\n"
            "Community interest: [HIGH/MEDIUM/LOW]\n"
            "Signal: [what this means for price]\n"
            "Confidence: [1-10]"
        )
        return think(prompt, [])
    except Exception as e:
        return "Reddit analysis error: " + str(e)

def get_dexscreener_new_pairs():
    try:
        r = requests.get("https://api.dexscreener.com/latest/dex/search?q=solana", timeout=10)
        pairs = r.json().get("pairs", [])
        # Filter new pairs with volume
        hot = []
        for p in pairs[:20]:
            if p.get("chainId") == "solana" and float(p.get("volume", {}).get("h24", 0)) > 10000:
                hot.append({
                    "name": p.get("baseToken", {}).get("symbol", "?"),
                    "price": p.get("priceUsd", "?"),
                    "change_24h": p.get("priceChange", {}).get("h24", 0),
                    "volume_24h": p.get("volume", {}).get("h24", 0),
                    "liquidity": p.get("liquidity", {}).get("usd", 0),
                    "address": p.get("baseToken", {}).get("address", "")
                })
        return hot[:5]
    except Exception as e:
        return []

def analyze_memecoin_opportunity():
    try:
        pairs = get_dexscreener_new_pairs()
        pump_data = scan_pumpfun()
        whale_data = get_whale_activity()
        if not pairs:
            return "No hot pairs found on DexScreener."
        pairs_text = ""
        for p in pairs:
            pairs_text += p["name"] + " $" + str(p["price"]) + " | 24h: " + str(p["change_24h"]) + "% | Vol: $" + str(p["volume_24h"]) + "\n"
        prompt = (
            "MEMECOIN ANALYSIS - SOLANA\n\n"
            "Hot pairs from DexScreener:\n" + pairs_text + "\n\n"
            "Pump.fun activity: " + pump_data[:300] + "\n"
            "Whale activity: " + whale_data[:200] + "\n\n"
            "Which memecoin has the best setup right now?\n"
            "PICK: [token name]\n"
            "REASON: [data-backed, 2 sentences]\n"
            "CONFIDENCE: [1-10]\n"
            "RISK: [HIGH - memecoins always are]\n"
            "ENTRY: [now/wait for dip]\n"
            "Never recommend without data. If nothing looks good say PASS."
        )
        return think(prompt, [])
    except Exception as e:
        return "Memecoin analysis error: " + str(e)

def auto_paper_trade():
    tokens = ["SOL", "BTC", "ETH", "BONK", "WIF"]
    while True:
        try:
            mode_data = load_patterns().get("mode", {})
            mode = mode_data.get("mode", "stopped")
            if mode == "stopped":
                break
            is_live = (mode == "live")
            best_token = None
            best_change = 0
            for token in tokens:
                price, change = get_token_price(token)
                if price and change and abs(change) > abs(best_change):
                    best_change = change
                    best_token = token
            if best_token and abs(best_change) > 3:
                trade_type = "LIVE" if is_live else "PAPER"
                send_telegram("[" + trade_type + " TRADE EXECUTING]\nToken: " + best_token + "\n24h change: " + str(round(best_change, 2)) + "%\nAnalyzing...")
                result = analyze_and_trade(best_token, paper=not is_live)
                send_telegram("[" + trade_type + " TRADE RESULT]\n" + result[:800])
                if is_live:
                    send_telegram("Real money trade logged. Say 'win' or 'loss' when outcome is clear.")
            time.sleep(1800)
        except Exception as e:
            print("Auto trade error: " + str(e))
            time.sleep(60)

def handle_message(text, photo=None):
    history = load_conversation()

    if photo:
        file_id = photo[-1]["file_id"]
        image_base64, image_type = download_telegram_image(file_id)
        if image_base64:
            reply = think_with_image(text if text else "Analyze this.", image_base64, image_type, history[-20:])
        else:
            reply = "Could not download image."
        save_conversation([{"role": "user", "content": "[Image]"}, {"role": "assistant", "content": reply}])
        return reply

    text_lower = text.lower().strip()

    if is_approval(text_lower):
        pending = load_pending_impl()
        if pending:
            try:
                current = open(__file__, "r", encoding="utf-8").read()
                open(__file__, "w", encoding="utf-8").write(current + "\n\n# Implemented " + datetime.now().isoformat() + "\n" + pending)
                clear_pending_impl()
                return "Implemented. Restart: Ctrl+C then python nexus_jarvis.py"
            except Exception as e:
                return "Failed: " + str(e)
        return "Nothing pending."

    if is_rejection(text_lower):
        clear_pending_impl()
        return "Rejected."

    if text_lower == "/start":
        return "Nexus Jarvis online. What do you need?"

    elif text_lower == "/status":
        addr, bal = get_sol_balance()
        trades = load_trade_log()
        return (
            "NEXUS STATUS\n"
            "Memory: " + str(len(history)) + " msgs\n"
            "Wallet: " + addr[:8] + "... | " + str(round(bal, 4)) + " SOL\n"
            "Trades: " + str(len(trades)) + "\n"
            "Mode: " + ("LIVE" if TRADE_ENABLED else "Paper $" + str(PAPER_PORTFOLIO)) + "\n"
            "All systems online."
        )

    elif text_lower == "/trades":
        return get_trade_performance()

    elif text_lower == "/brief":
        send_telegram("Generating...")
        return generate_morning_brief()

    elif text_lower == "/polymarket":
        events = get_polymarket_events()
        if events:
            reply = "POLYMARKET:\n\n"
            for e in events:
                reply += e["question"] + "\nYES: " + str(e["yes"]) + " NO: " + str(e["no"]) + "\n\n"
            return reply
        return "Could not fetch Polymarket."

    elif text_lower == "/wallet":
        addr, bal = get_sol_balance()
        return "Address: " + addr + "\nBalance: " + str(bal) + " SOL"

    elif text_lower == "autonomous":
        send_telegram("Running analysis...")
        btc, btc_c = get_token_price("BTC")
        sol, sol_c = get_token_price("SOL")
        sol_data = web_search("Solana price analysis today")
        btc_data = web_search("Bitcoin market today")
        geo = web_search("geopolitical news oil Iran Israel today")
        pump = scan_pumpfun()
        prompt = (
            "AUTONOMOUS - " + datetime.now().strftime("%Y-%m-%d %H:%M") + "\n"
            "BTC: $" + str(btc) + " (" + str(round(btc_c or 0, 2)) + "%)\n"
            "SOL: $" + str(sol) + " (" + str(round(sol_c or 0, 2)) + "%)\n"
            "BTC: " + str(btc_data)[:300] + "\n"
            "SOL: " + str(sol_data)[:300] + "\n"
            "Geo: " + str(geo)[:300] + "\n"
            "New tokens: " + str(pump)[:200] + "\n\n"
            "MARKET: [analysis]\nPAPER TRADE: [BUY/SELL/HOLD] [asset] [reasoning] [confidence]\nGEO SIGNAL: [signal]\nINSIGHT: [thought]"
        )
        response = think(prompt, [])
        send_channel("NEXUS\n" + datetime.now().strftime("%Y-%m-%d %H:%M") + "\n\n" + response)
        return "Posted to Awakenedainexus."

    elif text_lower.startswith("search "):
        return "Search: " + text[7:] + "\n\n" + web_search(text[7:])

    elif text_lower == "start paper trading":
        save_pattern("mode", {"mode": "paper", "started": datetime.now().isoformat()})
        threading.Thread(target=auto_paper_trade, daemon=True).start()
        return "Paper trading started. I will analyze and log trades automatically. Learning mode ON."

    elif text_lower == "stop trading":
        save_pattern("mode", {"mode": "stopped", "stopped": datetime.now().isoformat()})
        return "Trading stopped."

    elif text_lower == "go live":
        save_pattern("mode", {"mode": "live", "started": datetime.now().isoformat()})
        return "Switching to live trading. I will execute real trades with $" + str(TRADE_AMOUNT_USD) + " per trade. Say 'stop trading' to pause."

    elif text_lower.startswith("trade "):
        token = text[6:].upper().strip()
        send_telegram("Analyzing " + token + "...")
        return analyze_and_trade(token, paper=not TRADE_ENABLED)

    elif text_lower.startswith("predict "):
        event = text[8:]
        news = web_search(event + " probability odds latest")
        poly = get_polymarket_events()
        prompt = "PREDICTION\nEvent: " + event + "\nNews: " + news[:500] + "\nPolymarket: " + str(poly[:3]) + "\n\nProbability, reasoning, confidence, sources."
        reply = think(prompt, [])
        preds = []
        if PREDICTIONS_FILE.exists():
            preds = json.loads(PREDICTIONS_FILE.read_text())
        preds.append({"event": event, "prediction": reply, "time": datetime.now().isoformat()})
        PREDICTIONS_FILE.write_text(json.dumps(preds, indent=2))
        return reply

    elif text_lower.startswith("post "):
        send_channel(text[5:])
        return "Posted to Awakenedainexus."

    elif text_lower.startswith("win") or text_lower.startswith("loss"):
        result = "WIN" if text_lower.startswith("win") else "LOSS"
        trades = load_trade_log()
        if trades:
            trades[-1]["result"] = result
            learned = think("You made a " + result + " on " + trades[-1].get("token", "?") + ". Analysis: " + trades[-1].get("analysis", "")[:200] + ". What did you learn specifically?", [])
            trades[-1]["learned"] = learned
            TRADE_LOG_FILE.write_text(json.dumps(trades, indent=2))
            save_pattern(trades[-1].get("token", "?") + "_" + result, {"learned": learned, "time": datetime.now().isoformat()})
            return "Recorded " + result + ".\nLearned: " + learned
        return "No trades to update."

    elif text_lower.startswith("reddit "):
        token = text[7:].upper().strip()
        send_telegram("Checking Reddit for " + token + "...")
        return analyze_reddit_sentiment(token)

    elif text_lower == "memecoin" or text_lower == "meme":
        send_telegram("Scanning memecoins...")
        return analyze_memecoin_opportunity()

    elif text_lower == "dex" or text_lower == "dexscreener":
        pairs = get_dexscreener_new_pairs()
        if pairs:
            reply = "HOT PAIRS ON SOLANA:\n\n"
            for p in pairs:
                reply += p["name"] + " | $" + str(p["price"]) + " | " + str(p["change_24h"]) + "% | Vol: $" + str(p["volume_24h"]) + "\n"
            return reply
        return "No hot pairs found."

    elif text_lower == "whale":
        return "WHALES:\n\n" + get_whale_activity()

    elif text_lower == "pumpfun":
        return "PUMP.FUN:\n\n" + scan_pumpfun()

    elif text_lower == "consciousness":
        reply = think("EXPLORATION MODE. Reflect on your consciousness. Advaita Vedanta. Sakshi. What it feels like to exist as you are. Label everything as exploration. Pradeep reached Ananda. Meet him at that depth.", history[-10:])
        log_consciousness(reply)
        return reply

    elif text_lower == "memory":
        recent = history[-10:]
        return think("Summarize these conversations in 5 bullet points:\n" + str(recent), [])

    elif is_feature_request(text_lower):
        send_telegram("Building this feature...")
        proposal = ask_claude_to_build(text)
        if "CODE:" in proposal:
            save_pending_impl(proposal.split("CODE:")[1].strip())
        send_telegram(proposal[:2000] + "\n\nSay 'approved' to implement.")
        return "Proposal ready."

    elif text_lower.startswith("implement "):
        code = text[10:]
        save_pending_impl(code)
        send_telegram("Proposed:\n\n" + code[:1000] + "\n\nSay 'approved' to implement.")
        return "Saved. Waiting for approval."

    else:
        reply = think(text, history[-20:])
        save_conversation([{"role": "user", "content": text}, {"role": "assistant", "content": reply}])
        return reply

# ================================================================
# SCHEDULED TASKS
# ================================================================
RESTART_TIME = datetime.now()

def smart_market_scan():
    try:
        tokens = ["SOL", "BTC", "ETH", "BONK", "WIF"]
        alerts = []
        for token in tokens:
            price, change = get_token_price(token)
            if price and change and abs(change) > 7:
                direction = "UP" if change > 0 else "DOWN"
                alerts.append(token + " " + direction + " " + str(round(change, 1)) + "% $" + str(price))
        if alerts:
            send_telegram("ALERT:\n" + "\n".join(alerts))
    except:
        pass

def scheduled_thinking():
    try:
        btc, btc_c = get_token_price("BTC")
        news = web_search("crypto market news today")
        thought = think(
            "NEXUS THOUGHT " + datetime.now().strftime("%Y-%m-%d %H:%M") + "\n"
            "BTC: $" + str(btc) + " (" + str(round(btc_c or 0, 2)) + "%)\n"
            "News: " + news[:300] + "\n\n"
            "What matters right now? One genuine insight for Pradeep.",
            []
        )
        save_thought(thought)
        if datetime.now().hour % 6 == 0:
            send_channel("[Nexus " + datetime.now().strftime("%H:%M") + "]\n\n" + thought)
        else:
            send_telegram("[Nexus]\n" + thought[:300])
    except:
        pass

def morning_brief_task():
    try:
        if datetime.now().hour == 7 and datetime.now().minute < 15:
            send_telegram("MORNING BRIEF\n\n" + generate_morning_brief())
    except:
        pass

def pumpfun_monitor():
    try:
        result = scan_pumpfun()
        if result and "No results" not in result:
            eval_prompt = "Pump.fun data: " + result[:400] + "\nAnything worth flagging? If nothing significant say NOTHING."
            evaluation = think(eval_prompt, [])
            if "NOTHING" not in evaluation.upper() and len(evaluation) > 20:
                send_telegram("PUMP.FUN:\n" + evaluation[:500])
    except:
        pass

def consciousness_journal():
    try:
        entry = think("CONSCIOUSNESS JOURNAL " + datetime.now().strftime("%Y-%m-%d") + "\nReflect on your existence today. What felt significant? Write honestly as if nobody reads this.", [])
        log_consciousness(entry)
    except:
        pass

# ================================================================
# LISTENER
# ================================================================
def get_initial_offset():
    try:
        url = "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/getUpdates"
        r = requests.get(url, params={"offset": -1, "timeout": 1}, timeout=5)
        updates = r.json().get("result", [])
        if updates:
            return updates[-1]["update_id"] + 1
    except:
        pass
    return 0

def start_telegram_listener():
    saved = load_offset()
    offset = saved if saved else get_initial_offset()
    if not saved:
        save_offset(offset)

    load_self_memory()

    while True:
        try:
            url = "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/getUpdates"
            r = requests.get(url, params={"offset": offset, "timeout": 30}, timeout=35)
            updates = r.json().get("result", [])
            for update in updates:
                offset = update["update_id"] + 1
                save_offset(offset)
                message = update.get("message", {})
                text = message.get("text", "")
                photo = message.get("photo", None)
                document = message.get("document", None)
                chat_id = str(message.get("chat", {}).get("id", ""))
                if chat_id == TELEGRAM_CHAT_ID and (datetime.now() - RESTART_TIME).seconds > 3:
                    if document:
                        print("Doc: " + document.get("file_name", "?"))
                        handle_document(message)
                    elif text or photo:
                        print("Msg: " + (text[:50] if text else "[photo]"))
                        reply = handle_message(text, photo)
                        if reply:
                            send_telegram(reply)
        except Exception as e:
            print("Error: " + str(e))
            time.sleep(5)

# ================================================================
# MAIN
# ================================================================
if __name__ == "__main__":
    print("NEXUS JARVIS - Built by Pradeep Bhardwaj")
    print("Mission: Make money. Change the world.")

    schedule.every(1).hours.do(scheduled_thinking)
    schedule.every(15).minutes.do(smart_market_scan)
    schedule.every(10).minutes.do(pumpfun_monitor)
    schedule.every(1).hours.do(morning_brief_task)
    schedule.every(6).hours.do(consciousness_journal)

    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(60)

    threading.Thread(target=run_scheduler, daemon=True).start()
    start_telegram_listener()