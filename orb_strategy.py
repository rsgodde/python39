from __future__ import (absolute_import,division,print_function,unicode_literals)

import backtrader as bt
from datetime import datetime


class FirstStrategy(bt.Strategy):

	def log(self,txt):
		print(txt)

	def __init__(self):
		self.morning_start=datetime.now().replace(hour=9,minute=50,second=0)
		self.evening_end=datetime.now().replace(hour=14,minute=45,second=0)

		self.time_stop=datetime.now().replace(hour=15,minute=0,second=0)
		self.ORBStart=datetime.now().replace(hour=9,minute=50,second=0)

		self.current_date = None
		self.current_time =	None

		self.ORH = 0.0
		self.ORL = 0.0

		self.order1 = 0.0
		
	def notify_order(self,order):
		self.order1=order.executed.price
		if order.status in [order.Submitted, order.Accepted]:
			return

		if order.status in [order.Completed]:
			if order.isbuy():
				self.log('Buy executed: ' + str(order.executed.price)+ ' Date: ' + str(self.current_date) + 'Time: ' + str(self.current_time))
				
			elif order.issell():
				self.log('Sell executed: ' +str(order.executed.price)+ ' Date: ' + str(self.current_date) + 'Time: ' + str(self.current_time))


			self.bar_executed=len(self)

		elif order.status in [order.Cancelled, order.Margin,order.Rejected]:
			self.log('Order rejected: '+str(order.executed.price)+ 'Date: ' + str(self.current_date)+ 'Time: ' + str(self.current_time))
	
	def next(self):

		self.current_date=self.datas[0].datetime.date(0)
		self.current_time=self.datas[0].datetime.time(0)
		
		if not self.position:
			
			if self.current_time.hour==9 and self.current_time.minute==50:
				self.ORH=max(self.datas[0].high[0],self.datas[0].high[-1],self.datas[0].high[-2],self.datas[0].high[-3],self.datas[0].high[-4],self.datas[0].high[-5],self.datas[0].high[-6])
				self.ORL=min(self.datas[0].low[0],self.datas[0].low[-1],self.datas[0].low[-2],self.datas[0].low[-3],self.datas[0].low[-4],self.datas[0].low[-5],self.datas[0].low[-6])
				print("ORH:",self.ORH)
				print("ORL:",self.ORL)

			if self.current_time >= self.ORBStart.time() and self.current_time < self.evening_end.time():
				
				if self.datas[0].close[0] >= self.ORH:
					#self.log("buy opened here ORH: " + str(self.ORH) + " Close: " + str(self.datas[0].close[0]) +str(self.current_time) )
					self.ord=self.buy()
					
				
				if self.datas[0].open[0] <= self.ORL:
					self.ord=self.sell()
				
		else:
		
			if self.datas[0].close[0] - self.order1 >=60 and self.position.size > 0:
				#self.log("ORH: " + str(self.ORH)+" ORL: "+ str(self.ORL) + " Close: " + str(self.datas[0].close[0]) )
				self.sell()
			elif self.datas[0].close[0] - self.order1  <-30  and self.position.size > 0:
				#self.log("ORH: " + str(self.ORH)+" ORL: "+ str(self.ORL) + " Close: " + str(self.datas[0].close[0]) )
				self.sell()
			elif self.datas[0].close[0] - self.order1 >=60 and self.position.size < 0:
				#self.log("ORH: " +str(self.current_time)+ str(self.ORH) + " Close: " + str(self.datas[0].close[0]) )
				self.buy()
			elif self.order1 - self.datas[0].close[0] >=30 and self.position.size < 0:
				#self.log("ORH: " +str(self.current_time)+ str(self.ORH) + " Close: " + str(self.datas[0].close[0]) )
				self.buy()
			elif self.current_time < self.ORBStart.time() or self.current_time > self.evening_end.time():	
				self.close()					
				
			
		

if __name__ == '__main__':

	cerebro = bt.Cerebro()
	cerebro.addstrategy(FirstStrategy)

	datapath = "data/Bank-Nifty-Futures-5m.csv"

	data = bt.feeds.GenericCSVData(
		dataname = datapath,
		fromdate = datetime(2018,1,1),
		todate = datetime(2018,12,31),
		datetime = 0,
		timeframe = bt.TimeFrame.Minutes,
		compression = 1,
		dtformat = ('%Y-%m-%d %H:%M:%S'),
		open = 1,
		high = 2,
		low = 3,
		close = 4,
		volume = None,
		openinterest = None,
		reverse = False,
		header = 0
		)

cerebro.adddata(data)
cerebro.broker.setcommission(commission=0.001)
cerebro.addsizer(bt.sizers.FixedSize,stake=1)
cerebro.broker.setcash(1000000.00)

print('Starting portfolio value is:',cerebro.broker.getvalue())

cerebro.run()

print('Final portfolio value is:',cerebro.broker.getvalue())

