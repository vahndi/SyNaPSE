from sklearn.metrics import (
    explained_variance_score, mean_absolute_error, mean_squared_error, 
    median_absolute_error, r2_score
    )



class RegressionMetrics(object):
    
    @classmethod
    def get_metrics(cls, y_true, y_pred, 
                    sample_weight = None):
        
        """
        Returns typical metrics for regression from the sklearn.metrics module
        
        Inputs
        ------
        y_true: 
            array-like of shape = (n_samples) or (n_samples, n_outputs).
            Ground truth (correct) target values.
        y_pred:
            array-like of shape = (n_samples) or (n_samples, n_outputs).
            Estimated target values.
        sample_weight:
            array-like of shape = (n_samples), optional
            Sample weights.
        multioutput:
            string in ['raw_values', 'uniform_average', 'variance_weighted'] or 
            None or array-like of shape (n_outputs).
            Defines aggregating of multiple output scores. Array-like value 
            defines weights used to average scores. Default value correponds 
            to 'variance_weighted', this behaviour is deprecated since version 
            0.17 and will be changed to 'uniform_average' starting from 0.19.
            
            'raw_values' :
                Returns a full set of scores in case of multioutput input.
            'uniform_average' :
                Scores of all outputs are averaged with uniform weight.
            'variance_weighted' :
                Scores of all outputs are averaged, weighted by the variances 
                of each individual output.
        """
        metrics_dict = {}
        multioutputs2 = ['raw_values', 'uniform_average']
        multioutputs3 = ['raw_values', 'uniform_average', 'variance_weighted']

        metrics_dict['Explained Variance'] = {}
        for m in multioutputs3:
            metrics_dict['Explained Variance'][m] = explained_variance_score(
                y_true, y_pred, 
                sample_weight = sample_weight, 
                multioutput = m
                )

        metrics_dict['Mean Absolute Error'] = {}
        for m in multioutputs2:
            metrics_dict['Mean Absolute Error'][m] = mean_absolute_error(
                y_true, y_pred, 
                sample_weight = sample_weight, 
                multioutput = m
                )

        metrics_dict['Mean Squared Error'] = {}
        for m in multioutputs2:
            metrics_dict['Mean Squared Error'][m] = mean_squared_error(
                y_true, y_pred, 
                sample_weight = sample_weight,
                multioutput = m
                )

        metrics_dict['Median Absolute Error'] = median_absolute_error(
            y_true, y_pred
            )

        metrics_dict['Coefficient of Determination'] = {}
        for m in multioutputs3:
            metrics_dict['Coefficient of Determination'][m] = r2_score(
                y_true, y_pred, 
                sample_weight = sample_weight, 
                multioutput = m
                )

        return metrics_dict
