class SharedRouter:
    shared = ["auth", "contenttypes", "shared_tenant"]
    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.shared:
            return 'default'
        return None
    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.shared:
            return 'default'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.shared:
            return db == 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._state.db in self.shared and
            obj2._state.db in self.shared
        ):
            return True
        return None

class TenantRouter:
    def _get_client_db(self, model):
        if model._meta.app_label == 'council':
            return 'council_db'
        elif model._meta.app_label == 'admission':
            return 'admission_db'
        else:
            return 'default'
            
    def db_for_read(self, model, **hints):
        return self._get_client_db(model)

    def db_for_write(self, model, **hints):
        return self._get_client_db(model)