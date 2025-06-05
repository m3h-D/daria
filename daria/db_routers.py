class CustomRouter:
    mongo_apps = {'core'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.mongo_apps:
            return 'mongo'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.mongo_apps:
            return 'mongo'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        db_set = {self.db_for_read(obj1), self.db_for_read(obj2)}
        return len(db_set) == 1

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.mongo_apps:
            return db == 'mongo'
        return db == 'default'