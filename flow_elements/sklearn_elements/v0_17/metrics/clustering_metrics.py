from sklearn.metrics import (
    adjusted_mutual_info_score, adjusted_rand_score, completeness_score, 
    homogeneity_score, mutual_info_score, normalized_mutual_info_score, 
    silhouette_score, silhouette_samples, v_measure_score 
    )



class ClusteringMetrics(object):


    @classmethod
    def get_supervised_metrics(cls, labels_true, labels_pred):

        metrics_dict = {}
    
        metrics_dict['Mutual Information'] = {}
        metrics_dict['Mutual Information'
                    ]['Adjusted'] = adjusted_mutual_info_score(
                                                    labels_true, labels_pred
                                                    )
        metrics_dict['Mutual Information'
                    ]['Standard'] = mutual_info_score(labels_true, labels_pred)
        metrics_dict['Mutual Information'
                    ]['Normalized'] = normalized_mutual_info_score(
                                                    labels_true, labels_pred
                                                    )
    
        metrics_dict['Adjusted Rand Index'] = adjusted_rand_score(
                                                    labels_true, labels_pred
                                                    )
    
        metrics_dict['Completeness Score'] = completeness_score(
                                                    labels_true, labels_pred
                                                    )
    
        metrics_dict['Homogeneity Score'] = homogeneity_score(
                                                    labels_true, labels_pred
                                                    )
    
        metrics_dict['V Measure'] = v_measure_score(labels_true, labels_pred)
        
        
        return metrics_dict
    
    
    @classmethod
    def get_unsupervised_metrics(cls, inputs, pred_labels):
        
        metrics_dict = {}
        metrics_dict['Silhouette Score'] = {}
        for metric in ['cosine', 'manhattan', 'euclidean']:
            metrics_dict['Silhouette Score'][metric] = silhouette_score(
                                                        inputs.as_matrix(), 
                                                        pred_labels.as_matrix(), 
                                                        metric = metric
                                                        )

        return metrics_dict

