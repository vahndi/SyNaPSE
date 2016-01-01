from sklearn.metrics import (
    adjusted_mutual_info_score, adjusted_rand_score, completeness_score, 
    homogeneity_score, mutual_info_score, normalized_mutual_info_score, 
    silhouette_score, silhouette_samples, v_measure_score 
    )
from pandas import Series



class ClusteringMetrics(object):


    @classmethod
    def get_supervised_metrics(cls, labels_true, labels_pred):

        metrics_dict = {}
    
        mutual_information = Series(
            {'Adjusted': adjusted_mutual_info_score(labels_true, 
                                                   labels_pred),
             'Standard': mutual_info_score(labels_true, 
                                          labels_pred),
             'Normalized': normalized_mutual_info_score(labels_true, 
                                                       labels_pred)},
            name = 'Score')
        mutual_information.index.name = 'Type'
        metrics_dict['Mutual Information'] = mutual_information
            
        single_figures = Series(
            {'Adjusted Rand Index': adjusted_rand_score(labels_true, 
                                                        labels_pred),
             'Completeness Score': completeness_score(labels_true, 
                                                      labels_pred),
             'Homogeneity Score': homogeneity_score(labels_true, 
                                                    labels_pred) ,
             'V Measure': v_measure_score(labels_true, 
                                          labels_pred)},
            name = 'Score')
        single_figures.index.name = 'Type'
        metrics_dict['Single Figure'] = single_figures
        
        return metrics_dict
    
    
    @classmethod
    def get_unsupervised_metrics(cls, inputs, pred_labels):
        
        metrics_dict = {}
        
        silhouette = Series(
            {metric: silhouette_score(inputs.as_matrix(), 
                                      pred_labels.as_matrix(), 
                                      metric = metric)
             for metric in ['cosine', 'manhattan', 'euclidean']},
            name = 'Score'
        )
        silhouette.index.name = 'Type'
        metrics_dict['Silhouette Score'] = silhouette

        return metrics_dict

