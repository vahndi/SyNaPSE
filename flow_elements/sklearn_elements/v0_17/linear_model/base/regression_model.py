# Enaml
from custom_views.InputsTargetsSelector import InputsTargetsSelector_Model

# Models
from models_views.flowElement import FlowElement

# Other
from numpy import float64, int64
from pandasFunctions import joinInputsTargetsPredictions
from pandas import DataFrame, Series
from ...metrics.regression_metrics import RegressionMetrics as RM

# Preceding Elements
from flow_elements.LoadDataFrame import LoadDataFrame
from flow_elements.GetColumns import GetColumns



class RegressionModel(FlowElement):


    precedingElements = [LoadDataFrame, GetColumns]

    
    def set_inputs(self, dataFrame):
        
        self._dataFrame = dataFrame
        self.input_selector = InputsTargetsSelector_Model(
                                            dataFrame, 
                                            target_dtypes = [float64, int64]
                                            )
    
    
    def train_test_model(self):
        
        target_column = self.input_selector.selected_target()        
        
        # Split into training and test set
        X_train, y_train, X_test, self.y_test = \
        self.input_selector.get_training_test_data()
        
        # Train the model using the training sets
        self.estimator.fit(X_train, y_train)            
        y_pred_train = self.estimator.predict(X_train)
        self.y_pred_test = self.estimator.predict(X_test)            

        # Create a prediction summary dataframe
        self.df_predictions = joinInputsTargetsPredictions(
                                           train_inputs = X_train, 
                                           train_targets = y_train, 
                                           train_predictions = y_pred_train,
                                           test_inputs = X_test, 
                                           test_targets = self.y_test, 
                                           test_predictions = self.y_pred_test
                                           )
                                           
        self.df_targets_predictions = self.df_predictions[
                                                ['Target ' + target_column, 
                                                 'Predicted ' + target_column, 
                                                 'Set']]


    def get_attributes(self):
        
        input_columns = self.input_selector.checked_inputs()
        
        attributes = {}

        if hasattr(self.estimator, 'alpha_'):
            attributes['alpha'] = self.estimator.alpha_
        
        if hasattr(self.estimator, 'coef_'):
            attributes['coefficients'] = Series(index = input_columns,
                                                data =  self.estimator.coef_,
                                                name = 'coefficients')
        
        if hasattr(self.estimator, 'intercept_'):
            attributes['intercept'] = self.estimator.intercept_
            
        if hasattr(self.estimator, 'lambda_'):
            attributes['lambda'] = Series(index = input_columns,
                                          data =  self.estimator.lambda_,
                                          name = 'lambda')

        if hasattr(self.estimator, 'sigma_'):
            attributes['sigma'] = DataFrame(self.estimator.sigma_,
                                            index = input_columns,
                                            columns = input_columns)            

        if hasattr(self.uiModel, 'compute_score'):
            if self.uiModel.compute_score:
                attributes['scores'] = self.estimator.scores_

        return attributes

    
    def get_metrics(self):
        
        return RM.get_metrics(self.y_test, self.y_pred_test)

