using MarketParser;

var a = new Place().GetPlace("Оренбург Пятёрочка", 10);
Console.WriteLine(a.Result.features[0].properties.CompanyMetaData.address);