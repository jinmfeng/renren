import unittest
import repo_mysql 

class new_mysql(repo_mysql.repo_mysql):
	def clearTable(self):
		for table in self.table_name.values():
			self.cur.execute('drop table if exists {}'.format(table))
		self.conn.commit()
	exceed_seq=None
	def tag_exceed(self,rid,k,v):
		self.exceed_seq=(rid,k,v)
	def flush(self):
		self.exceed_seq=None

class test_repo_mysql(unittest.TestCase):

	def setUp(self):
		self.db=new_mysql()

	def tearDown(self):
		self.db.clearTable()
		self.db=None

	def test_save_friendList(self):
		names=[({'266754031':'王瑛','27331442':'Ethan.王哲','240303471':'刘洋English','239439171':'','222439171':'eeee','324134134':'～！@#￥%……&*（）'},6),(dict(),0),(None,None),({'3','4'},None)]
		for name,expt in names:
			self.assertEquals(self.db.save_friendList(name,'11111'),expt)

	def test_save_status(self):
		stats=[({'3352227193': {'cur_name': '張曉旭', 'timestamp': '2012-04-08 12:32', 'cur_content': '(img酷img)', 'orig_content': "you\'re ok. Let's do something\\", 'orig_name': '闷骚青年', 'orig_owner': '600992999', 'renrenId1': '410941086'}, 
			'2956159738': {'cur_name': '張曉旭', 'timestamp': '2012-01-08 00:58', 'cur_content': "'蛋舍k歌中'", 'orig_content': None, 'orig_name': None, 'orig_owner': None, 'renrenId1': '410941086'}, 
			'4268947468': {'cur_name': '張曉旭', 'timestamp': '2012-11-11 10:59', 'cur_content': '光棍节快乐 各位~', 'orig_content': None, 'orig_name': None, 'orig_owner': None, 'renrenId1': '410941086'}, 
			'3369389870': {'cur_name': '張曉旭', 'timestamp': '2012-04-11 17:59', 'cur_content': '哈哈转自(427674621,韩丹虹):转自(390845915,马焱意):恩 恩 @赵文轩帅哥，你火了耶～～转自(385023791,任慧)', 'orig_content': '南区的说 、物理系体操队 中间的男生好帅。 话说、中间的是赵文轩吧。。。好吧 应该的。(img流口水img)', 'orig_name': '任慧', 'orig_owner': '385023791', 'renrenId1': '410941086'}},4),(dict(),0),(None,None),({'3','4'},None)]
		for stat,expt in stats:
			self.assertEquals(self.db.save_status(stat,'11111'),expt)

	def test_save_history(self):
		log_info=('1111','profile','success','123')
		stat={'2956159738': {'cur_name': '張曉旭', 'timestamp': '2012-01-08 00:58', 'cur_content': "'蛋舍k歌中'", 'orig_content': None, 'orig_name': None, 'orig_owner': None, 'renrenId1': '410941086'}}
		#self.assertEquals(self.db.save_history(*log_info),1)
		self.assertEquals(self.db.save_friendList({'11':'name1'},'01','success'),1)
		self.assertEquals(self.db.save_status(stat,'02','timeout'),1)

	def test_save_profile(self):
		#tag in k, tag in v, tag in ignore
		expt=1
		pf={'gender': '女','大学': '北学-2013年-学院<br>理工大学-2011年-生命学院<br>'}
		self.assertEquals(self.db.save_profile(pf,'22222'),expt)
		self.assertEquals(self.db.exceed_seq,None)
		pf_exceed={'gender': '女','大学': '北学-2013年-学院<br>理工大学-2011年-生命学院<br>','qqq':'303923'}
		self.db.flush()
		self.assertEquals(self.db.save_profile(pf_exceed,'111'),expt)
		self.assertEquals(self.db.exceed_seq,('111','qqq','303923'))

	def test_read_cfg(self):
		cfg_filename='db_renren.ini'
		section_names={'friendList':{'renrenid2': 'varchar(15) NOT NULL'},'not_exist':None}
		default_value=repo_mysql.get_cfg_dict('DEFAULT')
		for section_name,expt in section_names.items():
			# no default value
			self.assertEquals(repo_mysql.get_cfg_dict(section_name,False),expt)
			# has default value
			res=repo_mysql.get_cfg_dict(section_name)
			if res is not None:
				expt.update(default_value)
			self.assertEquals(res,expt)

	def test_getSearched(self):
		stat1={'81': {'cur_name': 'name1', 'timestamp': '2012-01-08 00:58', 'cur_content': "'蛋舍k歌中'", 'orig_content': None, 'orig_name': None, 'orig_owner': None, 'renrenId1': '71'}}
		stat2={'82': {'cur_name': 'name1', 'timestamp': '2012-02-08 00:58', 'cur_content': "'蛋舍k歌中'", 'orig_content': None, 'orig_name': None, 'orig_owner': None, 'renrenId1': '72'}}
		self.db.save_friendList({'91':'name1'},'11','success')
		self.db.save_friendList({'92':'name2'},'12','timecost_info')
		self.db.save_friendList({},'13','timecost_info')
		self.db.save_friendList(None,'14','timeout')
		expt_friendList={'11','12','13'}
		self.db.save_status(stat1,'21','success')
		self.db.save_status(stat2,'22','timecost_info')
		self.db.save_status({},'23','timecost_info')
		self.db.save_status(None,'24','timeout')
		expt_status={'21','22','23'}

		self.assertEquals(self.db.getSearched('friendList'),expt_friendList)
		self.assertEquals(self.db.getSearched('status'),expt_status)

	def testGetRenrenId(self):
		name={'266754031':'王瑛','27331442':'Ethan.王哲','240303471':'刘洋English','239439171':'','222439171':'eeee','324134134':'～！@#￥%……&*（）'}
		name2={'231':'王瑛','2442':'Ethan.王哲','241':'刘洋English','2171':'','439171':'eeee','324134134':'～！@#￥%……&*（）'}
		renrenId='100032076'
		renrenId2='103076'
		self.db.save_friendList(renrenId,name)
		self.db.save_friendList(renrenId2,name2)

		self.assertEquals(self.db.getRenrenId(2,renrenId),set(name.keys()))
		self.assertEquals(self.db.getRenrenId(2,renrenId2),set(name2.keys()))
		self.assertEquals(self.db.getRenrenId(1,renrenId2),set())

	def test_getFriendList(self):
		name={'266754031':'王瑛','27331442':'Ethan.王哲','240303471':'刘洋English','239439171':'','222439171':'eeee','324134134':'～！@#￥%……&*（）'}
		name2={'231':'王瑛','2442':'Ethan.王哲','241':'刘洋English','2171':'','439171':'eeee','324134134':'～！@#￥%……&*（）'}
		renrenId='100032076'
		renrenId2='103076'
		self.db.save_friendList(name,renrenId)
		self.db.save_friendList(name2,renrenId2)

		self.assertEquals(self.db.getFriendList(renrenId),set(name.keys()))
		self.assertEquals(self.db.getFriendList(renrenId2),set(name2.keys()))

	def test_tableManage(self):
		self.db.clearTable()
		tableTag=['history','friendList','status','name']
		for tag in tableTag:
			self.db._init_table(tag)
			self.db._init_table(tag)
		self.db.clearTable()
		for tag in tableTag:
			self.db._init_table(tag)

if __name__=='__main__':
	suite=unittest.TestSuite()
	#suite.addTest(test_repo_mysql('testGetRenrenId'))

	#checked
	suite.addTest(test_repo_mysql('test_save_status'))
	suite.addTest(test_repo_mysql('test_save_friendList'))
	suite.addTest(test_repo_mysql('test_save_profile'))
	suite.addTest(test_repo_mysql('test_save_history'))
	suite.addTest(test_repo_mysql('test_getSearched'))
	suite.addTest(test_repo_mysql('test_getFriendList'))
	suite.addTest(test_repo_mysql('test_tableManage'))
	suite.addTest(test_repo_mysql('test_read_cfg'))

	runner=unittest.TextTestRunner()
	runner.run(suite)
