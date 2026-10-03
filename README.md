# Multi-Client Portfolio Management Platform

A centralized, multi-tenant Django web platform allowing an administrator to create, customize, publish, manage, and host professional portfolio websites for multiple clients from a unified SaaS dashboard.

---

## 🌟 Key Features

### 1. Unified SaaS Admin Dashboard
- **Role-Based Access Control**: Staff/Administrator authentication protecting all management routes.
- **Client Management Hub**: Create, edit, search, filter, publish/unpublish, and delete client portfolios.
- **Content Management**: Manage client projects, skill categories, work experience timelines, academic qualifications, and downloadable certificates.
- **Portfolio Link Management & Admin Sharing**:
  - Direct public URL display (`/p/<slug>/`).
  - **Copy Link**: One-click clipboard copy with animated toast notification ("Portfolio link copied!").
  - **Open Portfolio**: Opens public page in a new tab.
  - **Staff Preview**: View unpublished client draft portfolios with a distinct banner indicator.
  - **Social Sharing**: One-click share buttons for LinkedIn and Facebook.
  - **QR Code Generator**: Generates instant QR code pointing to the client's public portfolio URL.

### 2. Modern Dark-Theme Public Portfolio Page (`/p/<slug>/`)
- **No Client Account / Login Needed**: Public visitors and clients access published portfolios via their unique slug.
- **Dark Theme Aesthetics**: Charcoal/black backgrounds (`#0B0F17`), cyan/violet gradient glow FX, responsive cards, smooth transitions.
- **Open Graph Social Metadata**: Includes `og:title`, `og:description`, `og:image`, and `og:url` tags for optimal sharing previews on Facebook, LinkedIn, Twitter, and messaging apps.
- **Sections**:
  1. Hero Header (Headline, Profession, Profile Avatar, Call-To-Action buttons)
  2. About & Summary
  3. Categorized Skills & Tech Stack with percentage progress indicators
  4. Featured Projects Grid with live demo & GitHub repository links
  5. Work Experience Timeline
  6. Education & Qualifications Timeline
  7. Verified Downloads & Public Certificates
  8. Contact Section & Mailto integration
  9. Footer

### 3. Cloudinary File Upload & Private Access Security
- **Server-Side File Validation**:
  - Image formats: JPG, JPEG, PNG, WebP (Max 5 MB). Verified using Pillow image header decoding.
  - Document formats: PDF, DOC, DOCX (Max 10 MB). Verified using magic byte headers (`%PDF-`, OLECF, ZIP headers).
- **Public vs Private Files**:
  - `visibility="public"`: Delivered via Cloudinary URLs on published portfolio pages.
  - `visibility="private"`: Protected by server-side authentication (`/dashboard/files/<id>/download/`). Generates short-lived signed Cloudinary URLs.
- **Safe Asset Deletion**: Deleting or replacing a file cleans up Cloudinary assets and automatically updates associated Client `profile_image_url` or Project `featured_image_url` references.

---

## 🛠️ Required Technology Stack

- **Backend**: Python 3.12, Django 5.2 (LTS-compatible)
- **Database**: Neon PostgreSQL (via `dj-database-url` and `psycopg` 3.x), with automatic SQLite fallback for offline local testing
- **Media Storage**: Cloudinary SDK (`cloudinary`)
- **Frontend**: Django Templates, HTML5, Tailwind CSS (compiled CLI), Vanilla JavaScript, Lucide Icons
- **Static Asset Delivery**: WhiteNoise (`whitenoise`)
- **Hosting & Deployment**: Vercel (`@vercel/python` WSGI & `@vercel/static-build`)

---

## 🚀 Local Setup & Installation

### 1. Clone & Setup Virtual Environment
```bash
git clone https://github.com/your-username/portfolio_platform.git
cd portfolio_platform

# Create Python virtual environment
python -m venv .venv
.venv\Scripts\activate  # On Windows
# source .venv/bin/activate  # On Linux/macOS
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
npm install
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Set your environment variables in `.env`:
```env
DEBUG=True
SECRET_KEY=django-insecure-dev-local-secret-key-2026
ALLOWED_HOSTS=localhost,127.0.0.1,.vercel.app
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

# Database (Neon PostgreSQL) - leave empty for SQLite fallback during local dev
DATABASE_URL=postgres://user:password@ep-sample-123.us-east-2.aws.neon.tech/neondb?sslmode=require

# Cloudinary
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### 4. Build Tailwind CSS
```bash
npm run build:css
```

### 5. Run Database Migrations & Seed Sample Data
```bash
python manage.py makemigrations
python manage.py migrate
python scratch/seed_demo_data.py
```

### 6. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```
- **Admin Dashboard**: `http://127.0.0.1:8000/dashboard/` (Credentials: `admin` / `admin123`)
- **Public Sample Portfolio**: `http://127.0.0.1:8000/p/sherwin-sarmiento/`

---

## 🧪 Automated Testing & Verification

Run the automated test suite and security checks:

```bash
# 1. System check
python manage.py check

# 2. Check for missing migrations
python manage.py makemigrations --check

# 3. Run unit tests
python manage.py test

# 4. Run deployment check
python manage.py check --deploy
```

### Test Results Summary
- **Unit Tests**: 15 tests passed (100% success rate)
- **Coverage**: Client CRUD, Project CRUD, Unique slug collisions, Public vs Unpublished 404 security, Staff preview authorization, File extension & magic byte validation, Private download access control.

---

## ☁️ Vercel Deployment Instructions

### 1. Prerequisites
- A GitHub repository containing this codebase.
- A Neon PostgreSQL database instance (`DATABASE_URL`).
- A Cloudinary account (`CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`).

### 2. Deploying to Vercel
1. Log in to [Vercel](https://vercel.com) and click **Add New Project**.
2. Select your GitHub repository.
3. Configure the **Environment Variables** in Vercel settings:
   - `DEBUG`: `False`
   - `SECRET_KEY`: A strong 50+ character random string
   - `ALLOWED_HOSTS`: `.vercel.app,yourdomain.com`
   - `CSRF_TRUSTED_ORIGINS`: `https://*.vercel.app,https://yourdomain.com`
   - `DATABASE_URL`: `postgres://user:password@ep-sample-123.us-east-2.aws.neon.tech/neondb?sslmode=require`
   - `CLOUDINARY_CLOUD_NAME`: `your_cloud_name`
   - `CLOUDINARY_API_KEY`: `your_api_key`
   - `CLOUDINARY_API_SECRET`: `your_api_secret`
4. Deploy the project. Vercel automatically detects `vercel.json` and builds the static Tailwind CSS assets and WSGI Python function.

---

## 📋 Environment Variables Reference

| Variable | Required | Description |
|---|---|---|
| `DEBUG` | No (Default: `True`) | Set to `False` in production. |
| `SECRET_KEY` | Yes | Django cryptographic signing key. |
| `ALLOWED_HOSTS` | Yes | Comma-separated list of permitted host domains. |
| `CSRF_TRUSTED_ORIGINS` | Yes | Comma-separated trusted origins for POST requests. |
| `DATABASE_URL` | Yes (in Prod) | Neon PostgreSQL connection string with SSL mode. |
| `CLOUDINARY_CLOUD_NAME` | Yes | Cloudinary Cloud Name. |
| `CLOUDINARY_API_KEY` | Yes | Cloudinary API Key. |
| `CLOUDINARY_API_SECRET` | Yes | Cloudinary API Secret. |
