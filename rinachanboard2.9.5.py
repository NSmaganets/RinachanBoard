from scene import *
import sound
import random
import math
import ui
import csv
import  re
import time
import ast
import pathlib
import console
'''
#####################
璃奈ちゃんボードビューアー ver2.9.5
Rina-chan Board Viewer 
#####################
Created by @NSmagnets 
If you find some bugs,please send DM to my Twtter(@rinachanboard)



###########↓設定/config##########
'''

scriptFile='NoScript'  #./script/connect.csv
musicFile='NoMusic'  #./music/Rinachan.wav
timeduration=-0.02#時間ズレ補正単位は秒
sizemode=0    #0:縦を基準に　1:横幅を基準に合わせます。0が規定値
DEBUGMODE=False #True,False
boadcolor=[('#f6f6f6'),('#f400ff')] #ボードの色[白,ピンク]   
#boadcolor=[('#cdcdcd'),('#bb00c4')]
linecolor='#dadada'    #枠線の色.   
#boadcolor=[('#c9c9c9'),'#f400ff']

offsetX=52#x軸ズレ補正
offsetY=-10#y軸ズレ補正
blockSize=0#ブロックのサイズ。0の時、自動設定


selectmenu=True#Trueで選択画面を表示します。
'''
##########↑設定ここまで##########
'''



'''
  `               `                              `
  `                    `    `  ` `  `    `
    .i../<1 (+..(.,(..(.,...(,/ <.., (_;<+ .(``
  `                       `
  ` `    `  `  `    ` `       `       `       `
  ` `    `  jkk] `  `      `  ` kkk~          `
  `         JHm]          `     mHm~ `
  ` `       JHg] `  ` `       ` mHm~  `       `
  ` `    `  ?""= `  `           """`        ` `
    `    `  `  ` `  ` `   `   `       `     `  `
  `              dQQQQQQQQQQQQ;
                 dK         ,g{
  `               .W%.   ..W$  ` `  `
  `                 ,"(..J"      `  `    `
                      7""'  `  `
  `                    `    `    `  `    `
  `                            `    `
  `               ............., `       `



















'''


global scene
color=[]#[9_9,2_3,3_4]
boforecolor=[]
global boad


'''
scriptFile='./script/'+scriptFile
musicFile='./music/'+musicFile
'''
class option (object):  #メッセージ表示
	def errortext(MyScene,message):	
		 sound.stop_all_effects()
		 if str('コンソール') in message:
		  pass
		 else:
		  console.set_color(1.0, 0.0, 0.0)
		  print('【Error】: '+message)
		  console.set_color()
		 score_font = ('<System-Bold>', min(MyScene.size.w,MyScene.size.h)/35)
		 MyScene.score_label = LabelNode('0', score_font, parent=MyScene)
		 MyScene.score_label.position = (MyScene.size.w / 2, MyScene.size.h/8)
		 MyScene.score_label.z_position = 1
		 MyScene.score_label.color='#ff0000'
		 MyScene.score_label.text='ERROR!!  '+str(message)
		 MyScene.score_label.run_action(Action.sequence(
		 	Action.scale_by(0.2, 0.3,TIMING_EASE_IN_2),
		 Action.scale_to(1, 1,TIMING_EASE_IN_2),
		 Action.wait(3),
		 Action.scale_to(0, 2.5,TIMING_EASE_BACK_IN),
		 Action.remove()))
		 #MyScene.add_child(MyScene.score_label)
		 try:
		  MyScene.score_label2.remove_from_parent()
		  MyScene.triangle2.remove_from_parent()
		 except :
		  print('weq')

	def text1(MyScene,message,position,color,x):
		 score_font= ('Futura', min(MyScene.size.w,MyScene.size.h)/20*x)
		 MyScene.score_label1 = LabelNode('0', score_font, parent=MyScene)
		 MyScene.score_label1.position = position
		 MyScene.score_label1.z_position = 1
		 MyScene.score_label1.color=color
		 MyScene.score_label1.text=str(message)
		 MyScene.score_label1.run_action(Action.sequence(
		 Action.scale_to(1, 1,TIMING_EASE_IN_2),
		 Action.wait(2),
		 Action.fade_to(0,0.5),
		 Action.remove()))
		


class MyScene (Scene):

	def csv_import(self):
		tapp=[]
		ee=[]
		self.boadU=[]
		self.preset={}
		self.dataprev=[]
		with open('preset.csv') as f:#プリセットをインポート
		    reader = csv.reader(f)
		    l=[row for row in reader]
		    for yo in range(len(l)):
		     p=str(l[yo]).replace('["', '')
		     q=p.replace('"]','')
		     s1=q.replace("/'",'')
		     ss=ast.literal_eval(s1)
		     self.preset.update(ss)
		with open(scriptFile) as f:#スクリプトファイルをインポート
		    reader = csv.reader(f)
		    l=[row for row in reader]
		    qq=[]
		    for yo in range(len(l)):
		     if '<' in l[yo][0]:
		      pass
		     else:
		      self.dataprev.append([l[yo]])
		      tapp=[]
		      ee=[]
		      a=int(yo)
		      k=l[yo][1]
		      b=l[yo][2]
		      try:
		       c=float(l[yo][3])
		      except ValueError as err:
		         option.errortext(self,'スクリプトにエラーがあります。コンソールを確認してください。')
		         print(str('【Error】: スクリプト')+str(int(yo)+1)+str('行目:')+str(err)+str('←表示時間[sec]には必ず数字を入力。'))
		      if '_' in k:#プリセットを使用していない時
		       p=k.replace('(', '')
		       q=p.replace(')','')
		       m=q.replace('"','')
		       s=re.split(', ',m)
		      else:#プリセットを使用した時
		       p=re.split('//',k)#プリセットの要素を分ける
		       for e in p:
		        try:
		         qq=[self.preset[e][e1] for e1 in range(len(self.preset[e]))]#プリセットを検索して、座標を取得
		        except KeyError as err:
		         option.errortext(self,'スクリプトにエラーがあります。コンソールを確認してください。')
		         console.set_color(1.0, 0.0, 0.0)
		         print(str('\n【Error】: スクリプト')+str(int(yo)+1)+str('行目:')+str(err)+str('という名前のプリセットは、登録されていません。'))
		         console.set_color()
		         sound.play_effect('digital:PowerUp3')
		        ee.extend(qq)
		       s=[uu for uu in ee]
		      for i in s:
		       if type(i)==tuple:#万が一、座標情報がタプルだった場合(原則Stringのはずだが、万が一タプルが入ってしまった場合)
		        s1=str(i).replace("('",'')
		        s2=s1.replace("')",'')
		        s5=re.split('_',str(s2))
		        s6=[re.sub('\\D','',ty) for ty in s5]
		        print('u')
		       else:
		        s2=i.replace("/'",'')
		        s4=re.split('_',str(s2))
		       s3=(int(s4[0]),19-int(s4[1]))
		       tapp.append(s3)
		      self.boadU.append([a,tapp,b,c])
	
	def setup(self):#最初に実行される。設定画面uiの表示
		self.playing=False
		self.ready= False
		self.background_color='#c4c4c4'
		if selectmenu==True:
		 self.v = ui.load_view('select.pyui')

		 self.view.add_subview(self.v)
		 self.v.frame=(0,50,max(self.size.w/1.5,280),self.size.h/1.5)
		else:
		 try:
		  self.reboot()
		 except :
		  sound.play_effect('digital:PowerUp3')
		
	def reboot(self):#画面のマスを全て削除して再表示する。
		console.set_font()
		global offsetX,offsetY
		print(' 画面サイズ(横,縦):('+str(self.size.w)+','+str(self.size.h)+')')
		if blockSize==0:#縦幅を固定(横画面モード)
		 c=41#36.7
		 c=(self.size.h//25)+2
		 if sizemode==1:#横幅を固定(縦画面用モード)
		  c=(self.size.w//30)
		  offsetX=offsetX-2*c
		 elif sizemode==2:#璃奈ちゃんボード外枠付き
		  c=32
		  offsetX=101
		  offsetY=0
		  timeduration=0.03
		else:
		 c=blockSize
		self.alltime=0.0
		self.epoctime=0.0
		self.duration=0.0
		self.ready= False
		self.boad=[]
		try:
		 for i in self.block:
		  self.block[i].remove_from_parent()
		except :
		 pass
		self.block={}
		self.playing=False
		self.background_color = '#d9d9d9'
		#self.background_color = 'black'
		colorNo=0
		self.scenes=0
		self.touchcount=0
		#self.music=musicFile
		self.debugmode=DEBUGMODE
		self.onlights=[]
		self.offlights=[]
		self.dataprev=[]
		path = ui.Path()
		path.line_width = 3
		path.move_to(0, 0)
		path.line_to(0, self.size.h)
		path.close() 
		path2=ui.Path()
		path2.line_width = 1
		path2.move_to(0, 0)
		path2.line_to(0, c)
		path2.line_to(c, c)
		path2.line_to(c, 0)
		path2.close()
		for x in range(36):
			
			for y in range(28):
				self.rectangle3=ShapeNode(path2,fill_color=boadcolor[0],stroke_color=linecolor,position=(c*(x-1)+offsetX,c*y+offsetY))
				#self.rectangle = SpriteNode(boadtex[0], position=(c*x+10, c*y))
				z=(x-1,y)
				self.boad.append([z,colorNo])
				self.block[z]=self.rectangle3
				self.add_child(self.rectangle3)
		self.rectangle3.fill_color=boadcolor[1]
		z=(7,9)
		self.boadcopy=self.boad
		if self.debugmode==True:
		 score_font = ('Futura', c*0.9)
		 self.score_label2 = LabelNode('0', score_font, parent=self)
		 self.score_label2.position = (self.size.w / 2, self.size.h - 120)
		 self.score_label2.z_position = 1
		 self.score_label2.color='#0016ff'
		 self.add_child(self.score_label2)
		 self.score_label2.text='DEBUG MODE ver2.9.5 block='+str(c)
		 self.triangle2 = ShapeNode(path,fill_color='#66ffc3', stroke_color='#18a56e',position=(self.size.w/2, self.size.h/2), parent=self)
		 self.add_child(self.triangle2)
		 #self.block[z].texture=boadtex[1]
		 sound.play_effect('arcade:Coin_2')
		 sound.play_effect('tuut_02.wav')
		else:
		 sound.play_effect('piano:A3')
		self.csv_import()
		for i in range( len(self.boadU)):	
		 self.preload(i)
		#self.viewstatus(1)
		del offsetX,offsetY
		if sizemode==2:#外枠をつける
		 bby = SpriteNode('boad.png', position=(self.size.w/2, self.size.h/2),size=(self.size.w,self.size.h))
		 self.add_child(bby)
		sound.play_effect('game:Ding_3')
		print('【読み込み完了】')
		console.hud_alert('【読み込み完了】')
		option.text1(self,'Rina-chan Board Viewer',(self.size.w/2,self.size.h/2),'#8300bd',1)
		option.text1(self,'Tap to Start',(self.size.w/2,self.size.h/2-50),'#8300bd',0.8)
		console.set_font('VDL ロゴJrブラック',24)
		print('Rina-chan Board Viewer 🌈🎵')
		console.set_font()

	def preload(self,scene):#再生前にスクリプトを処理して、再生中の遅延を減らす。
		 global color
		 on=[]
		 off=[]
		 boforecolor=color
		 color=[]
		 v=self.boadU[int(scene)][1]
		 duration=self.boadU[int(scene)][3]
		 for www in self.boadcopy:
		  we=www[0]
		  if [we,0] in self.boadcopy:
		   ww=self.boadcopy.index([we,0])
		  else:
		   ww=self.boadcopy.index([we,1])
		  self.boadcopy[ww:ww+1]=[[we,0]]
		 for x in v:
		  y=[]
		  if [x,0] in self.boadcopy:
		   ww=self.boadcopy.index([x,0])
		  else:
		   ww=self.boadcopy.index([x,1])			  
		  tt=self.boadcopy[ww]
		  color.append(self.boadcopy[ww][0])
		 if boforecolor==None:
		  pass
		 else:
		  for bef in boforecolor:
		   if bef in color:
		     pass
		   else:
		    off.append(bef)
		 for co in color:
		  if co in boforecolor:
		    pass
		  else:
		   on.append(co)
		 self.onlights.append(on)#点灯させるマス
		 self.offlights.append(off)#消灯させるマス

		
		
	def r(self,sender):#設定画面ui
		 musicFormats=('.mp3','.wav','.m4a','.aiff','.webm','.flac')
		 sound.play_effect('digital:TwoTone2')
		 p = pathlib.Path('music')
		 q = pathlib.Path('script')
		 self.tableview1= sender.superview['tableview1']
		 self.tableview2= sender.superview['tableview2']
		 self.textview1= sender.superview['textview1']
		 self.modeselect=sender.superview['selectmode']
		 condition=' [設定状況]' +'\n scriptFile='+str(scriptFile)+ '\n musicFile='+str(musicFile)+ '\n\n timeduration='+str(timeduration)+'\n sizemode='+str(sizemode)+'\n DEBUGMODE='+str(DEBUGMODE)+'\n \n offsetX='+str(offsetX)+'\n offsetY='+str(offsetY)+'\n blocksize='+str(blockSize) +'\n \n boardColor='+str(boadcolor)+' \n lineColor='+str(linecolor)
		 self.textview1.text=str(condition)
		 print('############################ \n'+str(condition)+'\n############################\n\n')
		 listy=[p for p in p.iterdir() if p.is_file()and str(p).endswith(musicFormats) ] 
		 listz=[q for q in q.iterdir() if q.is_file() and str(q).endswith('.csv') ]
		 #print(y)
		 
		 ds = ui.ListDataSource(listy)
		 dd=ui.ListDataSource(listz)
		 
		 self.tableview1.data_source=ds
		 self.tableview1.reload()
		 self.tableview2.data_source=dd
		 self.tableview2.reload()

		 del musicFormats
		 try:
		  self.score_label2.remove_from_parent()
		  self.triangle2.remove_from_parent()
		 except :
		 	print('weq')

	def viewstatus(self,mode):#mode=0は設定画面uiに、mode=1はコンソールに現在の状態を表示		
		condition='[設定状況]' +'\n scriptFile='+str(scriptFile)+ '\n musicFile='+str(musicFile)+ '\n\n timeduration='+str(timeduration)+'\n sizemode='+str(sizemode)+'\n DEBUGMODE='+str(DEBUGMODE)+'\n \n offsetX='+str(offsetX)+'\n offsetY='+str(offsetY)+'\n blocksize='+str(blockSize) +'\n \n boardColor='+str(boadcolor)+' \n lineColor='+str(linecolor)

		if mode==0:
		 self.textview1.text=str(condition)
		elif mode==1:
		 print('############################ \n'+str(condition)+'\n############################\n\n')
	
	def go(self,sender):#設定画面の実行ボタンを押した時の処理。エラーチェックの後、self.setup()に進む。
		global  selectmenu
		selectmenu=False
		print(str('\n【読み込み開始】\n スクリプト:')+str(scriptFile)+str('\n 音源:')+str(musicFile))
		#print('Now Loading. Please wait...')
		sound.stop_all_effects()
		self.remove_all_actions()
		self.v.remove_subview(self.v)
		try:
		 self.reboot()
		except FileNotFoundError   as err:
		 err=str(' ファイルが選択されていないか、存在しません。\n')+str(err)
		 option.errortext(self,err)
		 for i in self.block:
		  self.block[i].remove_from_parent()
		 sound.play_effect('digital:PowerUp3')
		 selectmenu=True
		 self.remove_from_parent()
		 self.setup()
		except  IndexError as err:
		 err=str('スクリプトファイル内に空白行があります。<を補って下さい')
		 option.errortext(self,err)
		 sound.play_effect('digital:PowerUp3')
		 selectmenu=True
		 self.remove_from_parent()
		 self.setup()
		except KeyError as err:
		 err=str(err)+str('という名前のスクリプトは存在しません。')
		 option.errortext(self,err)
		 sound.play_effect('digital:PowerUp3')
		 selectmenu=True
		 self.remove_from_parent()
		 self.setup()
		except  UnicodeDecodeError as err:
		 err=str('スクリプトファイル内に使えない文字があります。\n 使える文字は英数字と記号のみです。\n')+str(err)
		 option.errortext(self,err)
		 sound.play_effect('digital:PowerUp3')
		 selectmenu=True
		 self.remove_from_parent()
		 self.setup()
		'''
		 except :
		 err=str('未知のエラーが発生しました。\n')
		 option.errortext(self,err)
		 sound.play_effect('digital:PowerUp3')
		 selectmenu=True
		 self.remove_from_parent()
		 self.setup()
		 '''
		
		
		##要修正##
	
	
	def yy(self,sender):#音源ファイルを選択するtableView
		sound.play_effect('digital:PowerUp2')
		global musicFile
		sel=sender.selected_row
		try:
		 item=self.tableview1.data_source.items[sel]
		 musicFile=str(item)
		 self.viewstatus(0)
		except :
		 option.errortext(self,'  始めにstartボタンを押してください。')
		
		

	def zz(self,sender):#スクリプトファイルを選択するtableView
			sound.play_effect('digital:PowerUp2')
			global scriptFile
			sel=sender.selected_row
			try:
			 item=self.tableview2.data_source.items[sel]
			 scriptFile=str(item)
			 self.viewstatus(0)
			except :
			 option.errortext(self,'  始めにstartボタンを押してください。')
		
	def segment(self,sender):#表示モードの選択をするslide bar
		global sizemode
		self.modeselect=sender.superview['selectmode']
		sizemode=  self.modeselect.selected_index
		try :
			self.viewstatus(0)
		except :
			option.errortext(self,'  始めにstartボタンを押してください。')
			
	def autoupdate(self,scenes):#手動更新時の処理
		 global color
		 boforecolor=color
		 color=[]
		 self.checkcolor= len(color+boforecolor)

		 v=self.boadU[int(self.scenes)-1][1]
		 duration=self.boadU[int(self.scenes)-1][3]
		 for www in self.boad:
		  we=www[0]
		  if [we,0] in self.boad:
		   ww=self.boad.index([we,0])
		  else:
		   ww=self.boad.index([we,1])
		  #tt=colored[ww]
		  self.boad[ww:ww+1]=[[we,0]]
		 for x in v:
		  y=[]
		  if [x,0] in self.boad:
		   ww=self.boad.index([x,0])
		  else:
		   ww=self.boad.index([x,1])			  
		  tt=self.boad[ww]
		  self.boad[ww:ww+1]=[[x,1]]
		  color.append(self.boad[ww][0])
		 if boforecolor==None:
		  pass
		 else:
		  for bef in boforecolor:
		   #buttonbg=sender.superview[bef]
		   if bef in color:
		     pass
		   else:
		   	self.block[bef].fill_color=boadcolor[0]
		 
		 for co in color:
		  #buttonbg=sender.superview[co]
		  if co in boforecolor:
		    pass
		  else:
		  	self.block[co].fill_color=boadcolor[1]
		 ssd=(time.time()-self.epoctime-self.alltime+self.duration)
		 
		 print('.                     .',ssd,self.scenes,str(self.checkcolor)+'Blocks')
		 if self.debugmode==False:
		  pass
		 else:
		  sse=int(ssd*1000)
		  self.score_label2.text=str(self.dataprev[self.scenes-1])+str(self.scenes)+'  '+str(sse)



	def autoupdate2(self,scenes):#自動更新時の処理
		 global color
		 if self.offlights==None:
		  pass
		 else:
		  for bef in self.offlights[self.scenes]:
		   self.block[bef].fill_color=boadcolor[0]
		 for co in self.onlights[self.scenes]:
		  self.block[co].fill_color=boadcolor[1]
		 self.scenes+=1
		 ssd=(time.time()-self.epoctime-self.alltime+self.duration)
		 print('.                     .',ssd,self.scenes)
		 if self.debugmode==False:#デバッグ画面の表示
		  pass
		 else:
		  sse=int(ssd*1000)
		  try :
		   self.score_label2.text='Auto'+str(self.dataprev[self.scenes-1])+str(self.scenes)+'  '+str(sse)	
		  except ValueError:#プリセットを使わなかった時
		   self.score_label2.text='Auto'+'  [ No preset ]   '+str(self.scenes)+'  '+str(sse)
		
		
	def timekeep(self,scenes):#経過時間の足し算
		 if self.scenes==len(self.boadU):#最終行に到達した時、update()が実行されないようにする。
		  self.ready=False
		  self.playing=False
		  if self.debugmode==True:
		   self.score_label2.text='session end'
		  
		 else:
		  self.duration=self.boadU[int(self.scenes)][3]
		  self.alltime =self.alltime + self.duration
		  self.autoupdate2(self.scenes)
		 
		
		
	def hideblock(self):#全ブロックを削除
		for i in self.block:
		 self.block[i].remove_from_parent()
		
			
	def did_change_size(self):#再生途中に画面の向きが変わると再生停止
		sound.stop_all_effects()
		self.ready=False
		self.playing=False
		#self.remove_all_actions()
		#self.setup()
		pass
	
	def update(self):#毎秒60回実行、ドット絵の遷移するタイミングを判定
		#self.T=time.time()	
		#print(self.T)
		if self.ready == True:#再生中のみ実行
		 if self.alltime+timeduration<= time.time()-self.epoctime:
		  self.timekeep(self.scenes)
		 
		 
		
		
	
	def touch_began(self, touch):#画面をタップした時の処理
		if selectmenu==False:
			if self.playing==False :#再生開始
			  global offsetX,offsetY,blockSize,linecolor,sizemode,scriptFile
			  try:
			   del offsetX,offsetY,blockSize,linecolor,sizemode,scriptFile,self.v,
			  except :
			   pass
			  self.scenes=0
			  self.alltime=0.0
			  for qwe in self.block.values():
			   qwe.fill_color=boadcolor[0]
			  sound.stop_all_effects()
			  sound.play_effect('arcade:Coin_4')
			  print('\n【再生開始】\n  フレーム表示誤差:')
			  time.sleep(1)
			  sound.play_effect(musicFile)
			  t=touch.location
			  self.playing=True
			  self.ready=True
			  self.epoctime=time.time()
			  self.timekeep(0)
			else:#再生中に3回タップした後、もう1回タップすると、リプレイ
			 self.touchcount+=1
			 if self.touchcount==3:
			  self.playing=False
			  self.touchcount=0
			 pass
			t=touch.location.x
			if self.debugmode==False :
				pass
			else:#デバッグモードの時、画面の右端をタップすると次の顔を、左端をタップすると1つ前の顔を表示。
			 
			 if self.scenes==len(self.boadU):#スクリプトの最終行に到達したら次の行には進まないようにする。
			  self.ready=False
			  self.playing=False
			  pass
			  
			 else:
			  
			  if self.size.w*0.1>=t:
			    print('prev')
			    self.ready=False
			    #self.playing=False
			    self.touchcount=0
			    self.scenes= self.scenes-1
			    #for qwe in self.block.values():
			     #qwe.fill_color=boadcolor[0]
			    self.autoupdate(self.scenes-1)
			    
			  else:
			   if self.size.w*0.9<=t:
			    print('next')
			    self.ready=False
			    #self.playing=True
			    self.touchcount=0
			    self.autoupdate2(self.scenes)
		  
			#print(t)
	def stop(self):#アプリを停止すると、動作を停止
	 sound.stop_all_effects()
	 try:
	  self.viewstatus(1)
	 except:
	  pass
	
	def touch_moved(self, touch):
		pass
	
if __name__ == '__main__':#MyScene()を実行
	run(MyScene(),'portrait', show_fps=True)
