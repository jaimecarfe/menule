from src.modelo.dao.UserDao import UserDao
from src.modelo.vo.LoginVO import LoginVO
from src.modelo.vo.UserVo import UserVo

class BussinessObject:
    def comprobarLogin(self, loginVO):
        logindao = UserDao()
        return  logindao.consultalogin(loginVO)
    
    def pruebainsert(self):
        user_dao = UserDao()
        