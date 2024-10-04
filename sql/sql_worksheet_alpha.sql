select x.CompanyID 'Company ID',
	x.CompanyName 'Company Name',
    y.Date,
    y.Open 'Stock Open',
    y.High 'Stock High',
    y.Close 'Stock Close',
    y.Volume 'Stock Volume',
    z.Price 'Dow Jones Price',
    z.Open 'Dow Jones Open',
    z.High 'Dow Jones High',
    z.Low 'Dow Jones Low',
    z.Volume 'Dow Jones Volumn',
    z.Change_Percent 'Dow Jones Change %'
from company_info x
	join stock_data y
    	on y.CompanyID = x.CompanyID
	join dow_jones z
    	on z.Date = y.Date
order by y.Date, x.CompanyID;