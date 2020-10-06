# polar

## Summary
* More than`60 000` non unique listings for properties were scraped from the web.

* Scraped information contains `area`, `number of rooms` `seller` type etc. followed by a `description` and `title`.

![image](https://github.com/besiobu/data-science-portfolio/blob/master/flats-in-cracow/img/feature_seller.png)

* The data is passed through a `etl` script that validates values and `extracts` certain `features` from the data.

![image](https://github.com/besiobu/data-science-portfolio/blob/master/flats-in-cracow/img/feature_parking.png)

* Due to high variability in the data I focused my efforts on forecasting flat prices.

* Certain assumptions about the data were made. The key one being that a `title` uniquely defines a listing.

* Furthermore missing data points in numerical columns a filled in with a `k nearest neighbours` imputer.

* Super expensive properties (`outliers`) are removed from the dataset.

* After carefully cleaining the data I obtained `4 500` data points about `flats`.

* Example features that were engineered:

| Name | Description |
|------|-------------|
| Log Area | The natural logarithm of the `Area` column |
| Total Rooms | The sum of `Rooms` and `Bathrooms` |
| Area to Rooms | The ratio of `Area` to `Rooms` |

* 4 models were trained on a containing `80%` of the data.

* `5-fold cross validation` was applied when tuning parameters.

* The models obtained the following scores:

| Name | Description | RMSE |
|------|-------------|-------|
| Baseline | Use mean to predict price | `222 475 PLN` |
| Gradient Boosting | Build decision trees to minimize error | `120 493 PLN` |
| Multi-layer Perception | Find weights in non linear function to minimize error | `119 237 PLN` |
| Voter | Linear combination of Gradient Boosting and Multi-layer perceptron | `116 478 PLN` |

* The model has issues predicting large properties. This may be caused by the simple fact that the more large (luxurious) the property the more potential factors could influence the price that are not in the datset.

![image](https://github.com/besiobu/data-science-portfolio/blob/master/flats-in-cracow/img/area_vs_amount.png)

* The model distinguishes between districts.

![image](https://github.com/besiobu/data-science-portfolio/blob/master/flats-in-cracow/img/district_vs_avg_amount.png)
