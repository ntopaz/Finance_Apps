import yfinance as yf
import pprint as pp

def main():
	spy = yf.download('SPY')
	#SPY.head()
	#pp.pprint(spy)
	spy_dict = spy.to_dict()
	#pp.pprint(spy_dict)

	starting_balance = 0
	monthly_investment = 2000
	red_day_threshold = .5
	max_investment_per_month = 1
	interest_rate_annual = 0.01
	interest_rate_daily = interest_rate_annual/365
	min_to_buy = monthly_investment/max_investment_per_month
	close = spy_dict["Close"]

	final_value,buys = buy_the_dip(starting_balance,monthly_investment, red_day_threshold, max_investment_per_month,close,min_to_buy,interest_rate_daily)
	asap_final,asap_buys = buy_asap(starting_balance,monthly_investment, red_day_threshold, max_investment_per_month,close)
	print("buy_the_dip: {}, Invest ASAP: {} for a total of {}% difference".format(final_value,asap_final,abs(1-final_value/asap_final)*100))
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
			print(date_obj)
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
	print(avg_days_btw_buys)
	print(interest_accrued)
	print(total_spent)
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
	print(total_spent)
	return(final_value,buys)


if __name__=="__main__":
	main()


	
	
	
