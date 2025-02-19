class HybridRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'shared_tenant':
            return 'shared_db'
        # Get current client DB from request
        return getattr(model, '_database', None) or 'council'  # Demo fallback

    def db_for_write(self, model, **hints):
        return self.db_for_read(model, **hints)

    def allow_relation(self, obj1, obj2, **hints):
        # Allow relations only within same DB
        return obj1._state.db == obj2._state.db

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'shared_tenant':
            return db == 'shared_db'
        return db in ['council_db', 'admission_db']  # Tenant DBs