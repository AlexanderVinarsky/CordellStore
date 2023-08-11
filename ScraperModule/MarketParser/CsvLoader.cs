using System.Globalization;
using System.Text;
using CsvHelper;
using CsvHelper.Configuration;

namespace MarketParser;

public static class CsvLoader {
    public static void SaveData(Root root, string path) {
        using var stream = new StreamWriter(path, false, Encoding.Unicode);
        using var csvWriter = new CsvWriter(stream, new CsvConfiguration(CultureInfo.InvariantCulture)
        {
            Delimiter = ","
        });
        csvWriter.WriteRecords(root.features);
    } 
}