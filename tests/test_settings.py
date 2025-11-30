# Test settings sets the schema to test

from core.config import Auth0Settings, KBCRemarketSettings, PostgresSettings, Settings


class SettingsTest(Settings):

    POSTGRES_SCHEMA: str = "api_test"

    # Auth0 settings
    auth0: Auth0Settings = Auth0Settings(
        AUTH0_DOMAIN="app.auth0.com",
        AUTH0_AUDIENCE="your-api-identifier",
        AUTH0_ISSUER="https://your-auth0-domain.auth0.com/",
    )

    postgres: PostgresSettings = PostgresSettings(
        POSTGRES_HOST="localhost",
        POSTGRES_USER="postgres",
        POSTGRES_PASSWORD="postgres",
        POSTGRES_DB="postgres",
        POSTGRES_SCHEMA=POSTGRES_SCHEMA,
    )

    kbc_remarket: KBCRemarketSettings = KBCRemarketSettings(
        KBC_USERNAME="kbc_username",
        KBC_PASSWORD="kbc_password",
        KBC_API_URL="https://api.kbc.com",
        KBC_SETUP_KEY="your_kbc_setup_key",
    )


test_settings = SettingsTest()
