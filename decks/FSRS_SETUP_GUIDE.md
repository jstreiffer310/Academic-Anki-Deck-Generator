# FSRS4Anki Setup Guide - The Smart Way to Study

## 🧠 What is FSRS?
**Free Spaced Repetition Scheduler** - An AI algorithm that predicts optimal review timing better than Anki's default. It learns from your actual performance to schedule cards more intelligently.

## 🚀 Installation Steps

### Step 1: Install FSRS4Anki Add-on
1. Open Anki
2. **Tools** → **Add-ons** → **Get Add-ons**
3. Click **"Browse Add-ons"**
4. Search: `"FSRS4Anki"`
5. Install the add-on by **open-spaced-repetition**
6. **Restart Anki**

### Step 2: Enable FSRS Algorithm
1. Go to **Tools** → **Preferences** → **Scheduling**
2. Check **"FSRS"** (this replaces Anki's default algorithm)
3. Set **"Desired retention"** to **0.85** (85% - good for exams)
4. Click **"Optimize FSRS parameters"** if you have review history
5. Click **OK**

### Step 3: Configure Your PSYC 2240 Decks
For each of your priority decks:

1. **Click on deck** → **Options** → **Advanced**
2. **FSRS settings:**
   ```
   Desired retention: 0.85 (85%)
   SM-2 retention: 0.90 (90%)
   FSRS parameters: (auto-optimized)
   ```

3. **New Cards:**
   ```
   Learning steps: 1m 10m
   Graduating interval: 3 days
   Easy interval: 4 days
   ```

4. **Reviews:**
   ```
   Easy bonus: 130%
   Interval modifier: 100%
   Maximum interval: 36500 days
   ```

## ⚙️ Optimal FSRS Settings for PSYC 2240

### High Priority Deck (Clinical/Core):
```
Desired retention: 0.90 (90% - higher for important stuff)
New cards/day: 25
Maximum reviews/day: 100
```

### Medium Priority Deck (Supporting):
```
Desired retention: 0.85 (85% - standard)
New cards/day: 20
Maximum reviews/day: 80
```

### Low Priority Deck (Background):
```
Desired retention: 0.80 (80% - lower is fine)
New cards/day: 15
Maximum reviews/day: 60
```

## 🎯 Why FSRS is Better for Your Exam

### Traditional Anki Algorithm:
- Fixed intervals (1, 6, 16, 35 days...)
- Same for everyone
- Doesn't learn from your performance

### FSRS Algorithm:
- **Adaptive intervals** based on YOUR performance
- **Learns your forgetting curve** for different types of content
- **Predicts optimal timing** using machine learning
- **Better retention** with fewer reviews

## 📊 FSRS Features You Should Use

### 1. Auto-Optimization
- **Tools** → **FSRS4Anki** → **Optimize parameters**
- Run this monthly to improve predictions
- Uses your review history to personalize scheduling

### 2. Retention Analysis
- **Tools** → **FSRS4Anki** → **True retention**
- Shows your actual retention rates
- Helps adjust desired retention settings

### 3. Load Balancing
- **Tools** → **FSRS4Anki** → **Load Balancer**
- Distributes reviews evenly across days
- Prevents review pile-ups before exams

### 4. Reschedule Existing Cards
- **Tools** → **FSRS4Anki** → **Reschedule**
- Updates all existing cards to use FSRS
- Do this after installing for immediate benefits

## 🎓 Study Strategy with FSRS

### Week 1-2: Setup Phase
1. Install FSRS and reschedule existing cards
2. Start with High Priority deck only
3. Let FSRS learn your patterns (do reviews consistently)

### Week 3-4: Expansion
1. Add Medium Priority deck
2. Run parameter optimization
3. Adjust desired retention if needed

### Week 5+: Optimization
1. Add Low Priority deck  
2. Use retention analysis to fine-tune
3. Focus on cards FSRS flags as "difficult"

### Before October 10th Exam:
1. Increase desired retention to 0.95 (95%) for cramming
2. Use load balancer to distribute final reviews
3. Trust FSRS scheduling - don't manually reschedule

## 🔧 Troubleshooting

### "FSRS option not showing"
- Make sure you installed the add-on AND restarted Anki
- Check Tools → Add-ons - FSRS4Anki should be listed and enabled

### "Parameters not optimizing"
- You need at least 1000 reviews for optimization
- If new user, use default parameters initially
- Optimization improves over time

### "Too many/few reviews"
- Adjust "Desired retention" (higher = more reviews)
- Use load balancer to smooth out daily reviews
- Check maximum reviews/day limits

## 🎯 Expected Results

### After 1 Week:
- FSRS learns your basic patterns
- Intervals start adapting to your performance
- More accurate predictions than default Anki

### After 1 Month:  
- Personalized parameters optimized
- Significantly better retention with fewer reviews
- Clear patterns in difficult vs easy content

### For October 10th Exam:
- **Optimal review timing** for maximum retention
- **Fewer wasted reviews** on easy cards
- **More focus** on cards you actually struggle with

## 💡 Pro Tips

1. **Be consistent** - FSRS learns from regular study patterns
2. **Use "Hard" button** when struggling - teaches FSRS about difficulty
3. **Don't skip days** - breaks the learning pattern
4. **Trust the algorithm** - resist urge to manually reschedule
5. **Run optimization monthly** - keeps parameters current

## 📚 Integration with Your PSYC 2240 Deck

Your priority-based deck structure works perfectly with FSRS:
- **High Priority cards** get more frequent reviews automatically
- **Clinical conditions** that you struggle with get extra attention  
- **Easy definitions** get longer intervals
- **Content analysis** + **FSRS learning** = optimal study efficiency

**FSRS will make your October 10th exam prep way more efficient!** 🧠📚

Generated: September 17, 2025
For: PSYC 2240 Fall 2025 Exam Prep