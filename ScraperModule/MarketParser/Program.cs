using MarketParser;

var a = Place.GetPlace("Москва долгопрудный продуктовый магазин", 50);
CsvLoader.SaveData(a.Result, "test.csv");