import java.util.Arrays;

public class Predictor {
    private int timePoint; // initialized dynamically
    private static int city; // static, can be updated as needed
    private String modelName; // should be set dynamically
    private static Double[] modelOutput; // static, will hold the forecast values
    static final String[] cityNames = {"ams", "arhnem", "assen", "groningen",
            "hague", "hertogenbosch", "leeuwarden", "lelystad", "maastricht", "middelburg",
            "utrecht", "zwolle"};

    public static Double[] getForecast(int timePoint, int cityIndex, String modelName) {
        if (modelName.equals("SARIMA")) {
            modelOutput = new Double[2]; // reset array
            modelOutput[0] = TrueValues.trueValues[cityIndex][timePoint];
            modelOutput[1] = ForecastSARIMA.forecast[cityIndex][timePoint];
        } else if (modelName.equals("LSTM")) {
            modelOutput = new Double[2]; // reset array
            modelOutput[0] = TrueValues.trueValues[cityIndex][timePoint];
            modelOutput[1] = ForecastLSTM.forecast[cityIndex][timePoint];
        }
        System.out.println(Arrays.toString(modelOutput));
        return modelOutput;
    }

    public static String getDate(int timePoint) {
        return TrueValues.dateTimeStrings[timePoint];
    }
}
