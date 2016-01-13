from ...sklearn_element import SKLearnElement
from pandas import DataFrame, Series
from numpy import squeeze



class ABCLinearModel(SKLearnElement):

    
    doc_root = \
    'http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.'
    

    def get_attributes(self):
        
        input_columns = self.input_selector.checked_inputs()
        
        attributes = {}

        if hasattr(self.estimator, 'active_'):
            attributes['active'] = self.estimator.active_

        if hasattr(self.estimator, 'alpha_'):
            attributes['alpha'] = self.estimator.alpha_
            
        if hasattr(self.estimator, 'alphas_'):
            attributes['alphas_'] = self.estimator.alphas_
        
        if hasattr(self.estimator, 'breakdown_'):
            attributes['breakdown'] =self.estimator.breakdown_
        
        if hasattr(self.estimator, 'coef_'):
            if self.estimator.coef_.ndim == 1:
                attributes['coefficients'] = Series(
                                        index = input_columns,
                                        data =  squeeze(self.estimator.coef_),
                                        name = 'coefficients'
                                        )
            else:
                attributes['coefficients'] = DataFrame(
                                        data =  self.estimator.coef_,
                                        columns = input_columns,
                                        index = self.labels
                                        )

        if hasattr(self.estimator, 'coef_path_'):
            attributes['coefficient_path'] = self.estimator.coef_path_
        
        if hasattr(self.uiModel, 'compute_score'):
            if self.uiModel.compute_score:
                attributes['scores'] = self.estimator.scores_        
        
        if hasattr(self.estimator, 'intercept_'):
            if self.estimator.intercept_.ndim == 0:
                attributes['intercept'] = self.estimator.intercept_
            else:
                attributes['intercept'] = Series(self.estimator.intercept_,
                                                 index = self.labels,
                                                 name = 'intercept')
            
        if hasattr(self.estimator, 'lambda_'):
            attributes['lambda'] = Series(index = input_columns,
                                          data =  self.estimator.lambda_,
                                          name = 'lambda')
                                          
        if hasattr(self.estimator, 'n_iter_'):
            if self.estimator.n_iter_ is not None:
                attributes['num_iterations'] = squeeze(self.estimator.n_iter_)

        if hasattr(self.estimator, 'n_subpopulation_'):
            attributes['n_subpopulation'] = self.estimator.n_subpopulation_

        if hasattr(self.estimator, 'sigma_'):
            attributes['sigma'] = DataFrame(self.estimator.sigma_,
                                            index = input_columns,
                                            columns = input_columns)            

        if hasattr(self.estimator, 'sparse_coef_'):
            attributes['sparse_coefficients'] = Series(
                                        index = input_columns,
                                        data =  self.estimator.sparse_coef_,
                                        name = 'sparse_coefficients'
                                        )

        return attributes