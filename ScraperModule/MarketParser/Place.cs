using System.Net;
using Newtonsoft.Json;

namespace MarketParser;

public class Place {
    public async Task<Root> GetPlace(string place, int count) {
        try {
            var locationRequest =
                $"https://search-maps.yandex.ru/v1/" +
                $"?apikey=a0a1e035-9501-415c-a135-2375d508d6a3" +
                $"&text={place}" +
                $"&lang=ru_RU" +
                $"&type=biz" +
                $"&results={count}";

            var locationResponse = await WebRequest.Create(locationRequest).GetResponseAsync();
            var location = "";

            await using (var stream = locationResponse.GetResponseStream())
            using (var reader = new StreamReader(stream))
                location = await reader.ReadToEndAsync();

            locationResponse.Close();
            return JsonConvert.DeserializeObject<Root>(location)!;
        }
        catch (Exception exception) {
            Console.WriteLine(exception);
        }

        return null!;
    }
}

public class Availability {
    public bool Everyday { get; set; }
    public bool TwentyFourHours { get; set; }
}

public class Category {
    public string @class { get; set; }
    public string name { get; set; }
}

public class CompanyMetaData {
    public string id { get; set; }
    public string name { get; set; }
    public string address { get; set; }
    public string url { get; set; }
    public List<Category> Categories { get; set; }
    public List<Phone> Phones { get; set; }
    public Hours Hours { get; set; }
}

public class Feature {
    public string type { get; set; }
    public Properties properties { get; set; }
    public Geometry geometry { get; set; }
}

public class Geometry {
    public string type { get; set; }
    public List<double> coordinates { get; set; }
}

public class Hours {
    public List<Availability> Availabilities { get; set; }
    public string text { get; set; }
}

public class Phone {
    public string type { get; set; }
    public string formatted { get; set; }
}

public class Properties {
    public ResponseMetaData ResponseMetaData { get; set; }
    public CompanyMetaData CompanyMetaData { get; set; }
    public string description { get; set; }
    public string name { get; set; }
}

public class ResponseMetaData {
    public SearchRequest SearchRequest { get; set; }
    public SearchResponse SearchResponse { get; set; }
}

public class Root {
    public string type { get; set; }
    public Properties properties { get; set; }
    public List<Feature> features { get; set; }
}

public class SearchRequest {
    public string request { get; set; }
    public int results { get; set; }
    public int skip { get; set; }
    public List<List<double>> boundedBy { get; set; }
}

public class SearchResponse {
    public int found { get; set; }
    public List<List<double>> boundedBy { get; set; }
    public string display { get; set; }
}