from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens
    
    @staticmethod
    def clear_takels():
        sql = "TRUNCATE TABLE takel;"
        return Database.execute_sql(sql)
    
    @staticmethod
    def add_takel(id, ip):
        sql = "INSERT INTO takel(takel_id, ip) VALUES(%s, %s)"
        params = [id, ip]
        return Database.execute_sql(sql, params)

    @staticmethod
    def add_controller(id, ip):
        sql = "INSERT INTO controller(controller_id, ip) VALUES(%s, %s)"
        params = [id, ip]
        return Database.execute_sql(sql, params)


    @staticmethod
    def get_takel_info (ip):
        sql = "SELECT takel_id, ip, subnet, universe, channel, CURR_POS FROM takel WHERE ip = %s"
        params = [ip]
        data=Database.get_rows(sql, params)
        return data

    @staticmethod
    def get_takel_by_id (id):
        sql = "SELECT takel_id, ip, subnet, universe, channel, CURR_POS FROM takel WHERE takel_id = %s"
        params = [id]
        data=Database.get_rows(sql, params)
        return data

    @staticmethod
    def update_ip(id, ip):
        sql = "UPDATE takel SET ip = %s WHERE takel_id = %s"
        params = [ip, id]
        return Database.execute_sql(sql, params)

    @staticmethod
    def update_chan(ip, val):
        sql = "UPDATE takel SET channel = %s WHERE ip = %s"
        params = [val, ip]
        return Database.execute_sql(sql, params)

    @staticmethod
    def update_sub(ip, val):
        sql = "UPDATE takel SET subnet = %s WHERE ip = %s"
        params = [val, ip]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def update_uni(ip, val):
        sql = "UPDATE takel SET universe = %s WHERE ip = %s"
        params = [val, ip]
        return Database.execute_sql(sql, params)
