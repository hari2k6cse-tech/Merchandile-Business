# 🍌 BANANA MERCHANDISE PORTAL - QUICK REFERENCE

## ⚡ 30-SECOND STARTUP

```bash
# Terminal 1: Start Backend
cd "c:\Hari\Merchandile Business\banana_portal\backend"
python main.py

# Terminal 2: Open Frontend
start chrome "file:///c:/Hari/Merchandile%20Business/banana_portal/frontend/index.html"
```

**Login:** `hari` / `hari`

---

## 🎯 CORE WORKFLOWS

### Adding a Harvest Entry
1. Click **"New Entry"** tab
2. Fill in date, variety, count, seller name
3. Enter expected amount
4. Select payment mode & status
5. (Optional) Add weight, vehicles, notes, actual amount
6. Click **"Save Entry"**
✓ Entry appears in table instantly
✓ Charts update automatically
✓ Summary cards recalculate

### Viewing Analytics
1. Click **"Analytics"** tab
2. View live charts:
   - Bar chart: Expected vs Actual (last 10)
   - Donut chart: Status breakdown
✓ Updates in real-time after new entries

### Checking All Entries
1. Click **"All Entries"** tab
2. Table shows all entries with:
   - Green rows = Profit
   - Red rows = Loss
3. Use **"Edit"** to modify
4. Use **"Delete"** to remove

### Editing an Entry
1. Click **"Edit"** on any row in table
2. Form fills with entry data
3. Modify any fields
4. Click **"Update Entry"**
✓ Changes saved immediately

---

## 📊 DASHBOARD CARDS

| Card | Meaning |
|------|---------|
| **Total Entries** | Number of harvest entries recorded |
| **Expected Revenue** | Sum of all expected amounts (₹) |
| **Actual Received** | Sum of all actual payments (₹) |
| **Net Profit/Loss** | Actual - Expected (Green=Profit, Red=Loss) |

---

## 🍌 BANANA VARIETIES (Tamil)

1. **பூவன்** - Poovan
2. **ரஸ்தாலி** - Robusta/Rasthali
3. **கத்தவள்ளி** - Karthali
4. **நேந்திரம்** - Nendran
5. **எலச்சி** - Elachi
6. **மொந்தன்** - Monthan

---

## 💳 PAYMENT MODES

- Cash
- UPI
- Bank Transfer
- Cheque
- Credit

---

## 📍 ENTRY STATUSES

1. **Transit in Progress** - On the way
2. **At Warehouse** - Stored at warehouse
3. **Delivered** - Reached destination
4. **Payment Pending** - Awaiting payment
5. **Partially Paid** - Partial payment received
6. **Fully Paid** - Complete payment received
7. **Cancelled** - Entry cancelled

---

## 🔗 QUICK API REFERENCE

```bash
# Test API Health
curl http://localhost:8000/api/health

# Get All Entries
curl http://localhost:8000/api/entries

# Get Summary
curl http://localhost:8000/api/analytics/summary

# Get Chart Data
curl http://localhost:8000/api/analytics/chart-data

# Get Status Breakdown
curl http://localhost:8000/api/analytics/status-breakdown
```

---

## 🆘 COMMON ISSUES & FIXES

| Issue | Solution |
|-------|----------|
| Backend won't start | Check if port 8000 is free |
| Login fails | Use exact: Username `hari`, Password `hari` |
| Charts blank | Refresh browser (Ctrl+F5) |
| No connection to backend | Ensure `python main.py` is running |
| Form won't submit | Fill all required fields (marked with *) |
| Delete asks for confirmation | Click "OK" to confirm deletion |

---

## 📁 FILE LOCATIONS

```
c:\Hari\Merchandile Business\banana_portal\
├── backend\main.py              ← Backend server
├── frontend\index.html          ← Open this in Chrome
├── test_api.py                  ← Run tests
├── banana_portal.db             ← Database (auto-created)
├── README.md                    ← Overview
├── DEPLOYMENT_GUIDE.md          ← Full guide
└── QUICK_REFERENCE.md           ← This file
```

---

## ✨ KEYBOARD SHORTCUTS

| Shortcut | Action |
|----------|--------|
| `Tab` | Move between form fields |
| `Enter` | Submit form |
| `Ctrl+F5` | Hard refresh browser |
| `F12` | Open developer console |

---

## 🎨 COLOR MEANINGS

- 🟢 **Green Row** = Profit (Actual > Expected)
- 🔴 **Red Row** = Loss (Actual < Expected)
- 🟡 **Yellow Button** = Primary action
- 🔵 **Blue Button** = Edit action
- 🔴 **Red Button** = Delete action

---

## 📈 BEST PRACTICES

1. **Daily Backup** - Export table data regularly
2. **Verify Numbers** - Check P&L calculations
3. **Update Status** - Keep status field current
4. **Add Notes** - Document special conditions
5. **Monitor Profit** - Review Net Profit/Loss regularly

---

## 🚀 PERFORMANCE TIPS

✓ Charts load faster on first entry click
✓ Use "All Entries" for searching
✓ Reload page if charts freeze
✓ Keep browser cache clear
✓ Use latest Chrome for best compatibility

---

## 📞 SUPPORT INFO

- **Backend Status:** http://localhost:8000/api/health
- **API Documentation:** See DEPLOYMENT_GUIDE.md
- **Testing:** Run `python test_api.py`
- **Logs:** Check browser console (F12)

---

**Last Updated:** 2026-04-17  
**Version:** 1.0.0  
**Status:** ✅ Production Ready
