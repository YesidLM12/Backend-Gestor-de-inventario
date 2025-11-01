from app.core.config import settings, print_settings

# Ver toda la configuración
print_settings()

# Acceder a valores individuales
print(f"\n🔑 Secret Key (primeros 10 chars): {settings.SECRET_KEY[:10]}...")
print(f"🗄️  Database: {settings.DATABASE_URL}")
print(f"🌐 CORS: {settings.BACKEND_CORS_ORIGINS}")
print(f"📧 Emails habilitados: {settings.emails_enabled}")