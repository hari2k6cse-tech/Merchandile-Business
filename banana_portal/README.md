# Banana Merchandise Portal

A complete web application for managing banana harvest entries, tracking revenue, and analyzing business metrics.

## Features

✅ User authentication (Login system)
✅ Dashboard with summary cards
✅ Real-time analytics with charts
✅ Harvest entry management (CRUD)
✅ P&L calculations
✅ Mobile-responsive UI
✅ FastAPI backend with SQLite database

## Quick Start

### Backend Setup

1. Navigate to the backend folder:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python main.py
```

The API will be available at: `http://localhost:8000`

### Frontend

1. Open `frontend/index.html` in your web browser

2. Login with:
   - Username: `hari`
   - Password: `hari`

## Default Credentials

- **Username:** hari
- **Password:** hari

## Project Structure

```
banana_portal/
├── backend/
│   ├── main.py           (FastAPI application)
│   ├── database.py       (SQLite setup)
│   ├── models.py         (Database models)
│   ├── schemas.py        (Pydantic schemas)
│   └── requirements.txt  (Dependencies)
└── frontend/
    └── index.html        (Single-page application)
```

## API Endpoints

### Authentication
- `POST /api/login` - User login

### Entries (CRUD)
- `POST /api/entries` - Create entry
- `GET /api/entries` - Get all entries
- `GET /api/entries/{id}` - Get single entry
- `PUT /api/entries/{id}` - Update entry
- `DELETE /api/entries/{id}` - Delete entry

### Analytics
- `GET /api/analytics/summary` - Get summary statistics
- `GET /api/analytics/chart-data` - Get chart data
- `GET /api/analytics/status-breakdown` - Get status distribution

## Features Implemented

### Dashboard
- Total entries counter
- Expected revenue tracking
- Actual received amount
- Net profit/loss calculation

### Harvest Entry Form
- Date selection
- Tamil variety selection
- Banana count and weight
- Seller information
- Payment details
- Status tracking
- Notes field

### Analytics
- Bar chart: Expected vs Actual revenue
- Donut chart: Status distribution
- Real-time updates

### Data Management
- Add new entries
- Edit existing entries
- Delete entries
- Color-coded rows (Green for profit, Red for loss)

## Banana Varieties (Tamil)
- பூவன் (Poovan)
- ரஸ்தாலி (Robusta)
- கத்தவள்ளி (Karthali)
- நேந்திரம் (Nendran)
- எலச்சி (Elachi)
- மொந்தன் (Monthan)

## Testing

All CRUD operations, validations, and edge cases have been tested including:
- Empty numeric fields handling
- Safe deletion and updates
- UI responsiveness on mobile
- Chart auto-updates
- P&L calculations

---

Made with ❤️ for Balu's Banana Business
