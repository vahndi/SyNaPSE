# Enaml
from custom_views.InputsTargetsSelector import InputsTargetsSelector_Model

# Models
from linear_model import ABCLinearModel

# Other
from numpy import int64
from modules.pandas_helpers import join_inputs_targets_predictions
from pandas import DataFrame
from ...metrics.classification_metrics import ClassificationMetrics as CM
from sklearn.metrics import confusion_matrix



class ABCClassificationModel(ABCLinearModel):

    
    def set_inputs(self, dataframe):
        
        self._dataframe = dataframe
        self.input_selector = InputsTargetsSelector_Model(
                                            dataframe, 
                                            target_dtypes = [int64, object]
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

        # Create confusion matrices
        self.labels = sorted(self._dataframe[target_column].unique())
        self.confusion_matrix_train = DataFrame(
                            confusion_matrix(y_train,  y_pred_train),
                            index = self.labels,
                            columns = self.labels
                            )
        self.confusion_matrix_test = DataFrame(
                            confusion_matrix(self.y_test, self.y_pred_test),
                            index = self.labels,
                            columns = self.labels
                            )

        # Create a prediction summary dataframe
        self.df_predictions = join_inputs_targets_predictions(
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
    
    def get_metrics(self):

        return CM.get_metrics(self.y_test, self.y_pred_test,
                              'multiclass') # TODO: pass the right classification type


    def getOutputs(self):

        try:

            # Assign local variables
            args = self.getArgs()
            
            # Validate inputs
            if not self.input_selector.validate_inputs():
                return {'Outputs': 'No Outputs'}              

            # Create Logistic Regression model
            self.estimator = self.estimator_type(** args)
            self.train_test_model()
    
            # Return outputs 
            attributes = self.get_attributes()
            metrics = self.get_metrics()       

            
            return {'Attributes': attributes,
                    'Metrics': metrics,
                    'dataframe': self.df_predictions,
                    'Target vs. Predicted': self.df_targets_predictions,
                    'Confusion Matrix': 
                        {'training': self.confusion_matrix_train,
                         'test': self.confusion_matrix_test}
                    }

        except Exception as e:
                
            return {'Exception':{'__class__': str(e.__class__),
                                 '__doc__': e.__doc__,
                                 'message': e.message}}