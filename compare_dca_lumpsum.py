#!/usr/bin/env python3
import yfinance as yf
import pprint as pp
import argparse

def main():
	parser = argparse.ArgumentParser(description="Compare investing strategy of buying on 1st of month versus on first occuring red days")
	parser.add_argument("-b","--starting_balance",help="Starting amount (default=0)", default=0)
	parser.add_argument("-a","--monthly_investment",help="Dollar amount to invest each month (default=500)",default=500)
	parser.add_argument("-t","--red_day_threshold",help="Red day threshold - invest if security drops at least this much in percentage (default=0.5%%)",default=.5)
	parser.add_argument("-m","--max_times_to_invest_each_month",help="Invest money over the course of the first occuring N red days (default=2)",default=2)
	parser.add_argument("-s","--stock",help="Stock or ETF to run this analysis for (from Yahoo finance API)",required=True)
	parser.add_argument("-i","--interest",help="Assumed annual savings interest rate to keep money in while waiting to invest it (default=1%%)",default=1)
	args = vars(parser.parse_args())
	### Print Args ###
	print ("Compare investing strategy of buying on 1st of month versus on first occuring red days")
	print("v1.0")
	print("#######################################################################################################")
	print ("Running with the following parameters:")
	for arg in args:
		print (arg,":",args[arg])
	
	
	starting_balance = args["starting_balance"]
	stock= args["stock"]
	monthly_investment = args["monthly_investment"]
	red_day_threshold = args["red_day_threshold"]
	max_investment_per_month = args["max_times_to_invest_each_month"]
	interest_rate_annual = float(args["interest"]/100)
	
	interest_rate_daily = interest_rate_annual/365
	min_to_buy = monthly_investment/max_investment_per_month
	stock_data = yf.download(stock)
	data_dict = stock_data.to_dict()
	close = data_dict["Close"]

	final_value,buys = buy_the_dip(starting_balance,monthly_investment, red_day_threshold, max_investment_per_month,close,min_to_buy,interest_rate_daily)
	asap_final,asap_buys = buy_asap(starting_balance,monthly_investment, red_day_threshold, max_investment_per_month,close)
	difference = abs(1-final_value/asap_final)*100
	if final_value > asap_final:
		print("Buy on red days beat buying ASAP: ${} vs ${} for a difference of {}%".format(final_value,asap_final,difference))
	if final_value <= asap_final:
		print("Buying ASAP beat buying only on red days: ${} vs ${} for a difference of {}%".format(asap_final,final_value,difference))
	with open("output_file.txt","w") as f:
		f.write("Month_year\tbuy_the_dip\tasap\n")
		for month_year in buys:
			f.write("{}\t{}\t{}\n".format(month_year,buys[month_year],asap_buys[month_year]))

def buy_the_dip(starting_balance,monthly_investment, red_day_threshold, max_investment_per_month,close,min_to_buy,interest_rate_daily):
	current_close = 0
	current_month = 0
	first = True
	total_spent = 0
	avg_days_btw_buys = []
	days_elapsed = 0
	interest_accrued = 0
	buys={}
	for date_obj in close:
		#print(date_obj)
		if first:
			first = False
			print("Data goes as far back as {}".format(date_obj))
			continue
		if current_close == 0:
			current_close = close[date_obj]
			current_month = date_obj.month
			investment = monthly_investment
			shares = 0
			continue
		if investment >0:
			days_elapsed +=1			
		if current_month == date_obj.month:
			if investment > 0:
				if close[date_obj] < current_close:
					percent_difference = abs(1-close[date_obj]/current_close)*100
					#print(current_close,close[date_obj],percent_difference)
					if percent_difference >= red_day_threshold:
						month_year = "{}_{}".format(date_obj.month,date_obj.year)
						if investment <= min_to_buy:
							shares_bought = (investment/float(close[date_obj]))
							shares = shares + shares_bought
							total_spent += investment
							investment = 0
							avg_days_btw_buys.append(days_elapsed)
							days_elapsed = 0
							buys[month_year] = shares*close[date_obj]
						else:
							shares_bought = ((investment/max_investment_per_month)/float(close[date_obj]))
							shares = shares + shares_bought
							total_spent += investment/max_investment_per_month
							investment = investment - (investment/max_investment_per_month)
							avg_days_btw_buys.append(days_elapsed)
							days_elapsed = 0
							buys[month_year] = shares*close[date_obj]
					else:
						interest_accrued = interest_accrued + (interest_rate_daily*investment)
				else:
					interest_accrued = interest_accrued + (interest_rate_daily*investment)
		else:
			investment = investment + monthly_investment
			current_month = date_obj.month
	#	print(date_obj,investment)
		current_close = close[date_obj]
	final_value = shares*current_close
	avg_days_btw_buys = sum(avg_days_btw_buys)/len(avg_days_btw_buys)
	#print(avg_days_btw_buys)
	#print(interest_accrued)
	print("Total invested buying on red days ${}".format(total_spent))
	return(final_value,buys)

def buy_asap(starting_balance,monthly_investment, red_day_threshold, max_investment_per_month,close):
	current_close = 0
	current_month = 0
	total_spent = 0
	shares=0
	first = True
	buys={}
	for date_obj in close:
		#print(date_obj)
		if first:
			first = False
			continue
		month_year = "{}_{}".format(date_obj.month,date_obj.year)
		if current_close == 0:
			current_close = close[date_obj]
			current_month = date_obj.month
			investment = monthly_investment
			shares = shares + (investment/float(close[date_obj]))	
			total_spent += investment
			buys[month_year] = shares*close[date_obj]
			continue
		if current_month != date_obj.month:
			shares = shares + (investment/float(close[date_obj]))	
			total_spent += investment
			#print(date_obj,investment,shares)
			current_month = date_obj.month
			buys[month_year] = shares*close[date_obj]
		current_close = close[date_obj]
	final_value = shares*close[date_obj]
	print("Total invested buying asap ${}".format(total_spent))
	return(final_value,buys)


if __name__=="__main__":
	main()


	
	
	
