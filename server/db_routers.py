import threading

tenant_local = threading.local()

class TenantRouter:
    shared_apps = ["auth", "contenttypes", "shared_tenant"]

    def _get_tenant(self):
        return getattr(tenant_local, 'tenant', None)

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.shared_apps:
            return 'default'
        tenant = self._get_tenant()
        return tenant.database_name if tenant else None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.shared_apps:
            return 'default'
        tenant = self._get_tenant()
        return tenant.database_name if tenant else None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.shared_apps:
            return db == 'default'
        tenant = self._get_tenant()
        return db == tenant.database_name if tenant else None

    def allow_relation(self, obj1, obj2, **hints):
        db1 = obj1._state.db
        db2 = obj2._state.db
        if db1 == db2:
            return True
        # Allow relations if one object is in the default DB and the other is in a tenant DB
        if 'default' in [db1, db2] and (db1 in self.shared_apps or db2 in self.shared_apps):
            return True
        return None