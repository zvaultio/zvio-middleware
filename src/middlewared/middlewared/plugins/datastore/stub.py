from middlewared.service import Service, private


class DatastoreStubService(Service):
    
    class Config:
        namespace = 'datastore.stub'
    """
    Stub service to handle queries for removed database tables.
    """

    @private
    async def query_system_failover(self, filters=None, options=None):
        """
        Stub implementation for the system.failover table which has been removed.
        Returns an empty list or a default object based on the options.
        """
        self.logger.debug('Stub query for removed system.failover table')
        
        if options and options.get('get'):
            # Return a default object if 'get' is True
            return {
                'id': 1,
                'disabled': True,
                'master': False,
            }
        
        # Return an empty list by default
        return []

    @private
    async def update_system_failover(self, id_value, values, options=None):
        """
        Stub implementation for updating the system.failover table which has been removed.
        Returns the updated values as if the update was successful.
        """
        self.logger.debug('Stub update for removed system.failover table')
        return values

    @private
    async def insert_system_failover(self, values, options=None):
        """
        Stub implementation for inserting into the system.failover table which has been removed.
        Returns 1 as if the insert was successful.
        """
        self.logger.debug('Stub insert for removed system.failover table')
        return 1

    @private
    async def delete_system_failover(self, id_value, options=None):
        """
        Stub implementation for deleting from the system.failover table which has been removed.
        Returns True as if the delete was successful.
        """
        self.logger.debug('Stub delete for removed system.failover table')
        return True

    @private
    async def handle_removed_tables(self, name, filters=None, options=None):
        """
        Handle queries for tables that have been removed from the database.
        Returns None if the table is not handled by this stub service.
        """
        if name == 'system.failover':
            return await self.query_system_failover(filters, options)
        
        return None

    @private
    async def handle_removed_tables_update(self, name, id_value, values, options=None):
        """
        Handle updates for tables that have been removed from the database.
        Returns None if the table is not handled by this stub service.
        """
        if name == 'system.failover':
            return await self.update_system_failover(id_value, values, options)
        
        return None

    @private
    async def handle_removed_tables_insert(self, name, values, options=None):
        """
        Handle inserts for tables that have been removed from the database.
        Returns None if the table is not handled by this stub service.
        """
        if name == 'system.failover':
            return await self.insert_system_failover(values, options)
        
        return None

    @private
    async def handle_removed_tables_delete(self, name, id_value, options=None):
        """
        Handle deletes for tables that have been removed from the database.
        Returns None if the table is not handled by this stub service.
        """
        if name == 'system.failover':
            return await self.delete_system_failover(id_value, options)
        
        return None
