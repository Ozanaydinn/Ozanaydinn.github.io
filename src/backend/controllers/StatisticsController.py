from global_data import r_envoy

class StatisticsController:
    parser = reqparse.RequestParser()
    parser.add_argument('session_id', help = 'This field cannot be blank', required = True)

    @jwt_required
    def post(self, course_id):
        data = self.parser.parse_args()
        
        session_id = data['session_id']
        #continue





