from sklearn.metrics import (
    accuracy_score, average_precision_score, confusion_matrix, f1_score, 
    fbeta_score, hamming_loss, hinge_loss, jaccard_similarity_score, log_loss, 
    matthews_corrcoef, precision_recall_curve, precision_recall_fscore_support, 
    precision_score, recall_score, roc_auc_score, roc_curve, zero_one_loss
    )
from pandas import DataFrame



class ClassificationMetrics(object):


    binary_metrics = {matthews_corrcoef, precision_recall_curve, roc_curve, 
                      average_precision_score, roc_auc_score}
    multiclass_metrics = {confusion_matrix, hinge_loss}
    multilabel_metrics = {accuracy_score, hamming_loss, 
                          jaccard_similarity_score, log_loss, 
                          precision_recall_fscore_support, precision_score,
                          recall_score, zero_one_loss, average_precision_score,
                          roc_auc_score}
    metrics = {'binary': binary_metrics,
               'multiclass': multiclass_metrics,
               'multilabel': multilabel_metrics}


    @classmethod
    def get_metrics(cls, y_true, y_pred, classification_type, y_proba = None,
                    normalize = True, sample_weights = None,
                    labels = None, pos_label = 1, beta = None, 
                    classes = None, eps = 1e-15, 
                    warn_for = ('precision', 'recall', 'f-score')):
        """
        Returns dicts of scores and losses relating to classification metrics
        
        Inputs
        ------
        y_true:
            Ground truth (correct) labels.
        y_pred:
            Predicted labels, as returned by a classifier.  
        y_proba:
            Predicted class probabilities, as returned by a classifier.
        classification_type:
            'binary', 'multiclass' or 'multilabel'        
        normalize:
            bool, optional (default=True)
            If False, return the number of correctly classified samples. 
            Otherwise, return the fraction of correctly classified samples.
        sample_weights:
            array-like of shape = [n_samples], optional
            Sample weights.
        labels:
            list, optional
            The set of labels to include when average != 'binary', and their 
            order if average is None. Labels present in the data can be 
            excluded, for example to calculate a multiclass average ignoring a 
            majority negative class, while labels not present in the data will 
            result in 0 components in a macro average. For multilabel targets, 
            labels are column indices. By default, all labels in y_true and 
            y_pred are used in sorted order.
            Changed in version 0.17: parameter labels improved for multiclass 
            problem.
        pos_label:
            str or int, 1 by default
            The class to report if average == 'binary'. Until version 0.18 it 
            is necessary to set pos_label = None if seeking to use another 
            averaging method over binary targets.
        average:
            None or string, ['binary' (default), 'micro', 
                             'macro', 'samples', 'weighted']
            This parameter is required for multiclass/multilabel targets. See
            scikit-learn documentation for (extensive) details
        beta:
            Weight of precision in harmonic mean for F-beta score        
        classes:
            array, shape = [n_labels], optional
            Integer array of labels.
        eps:
            Log loss is undefined for p = 0 or p = 1, so probabilities are 
            clipped to max(eps, min(1 - eps, p)).
        warn_for:
            tuple or set, for internal use
            This determines which warnings will be made in the case that the 
            precision_recall_fscore_support function is being used to return 
            only one of its metrics.
        """
        
        scores_dict = {}
        losses_dict = {}
        metrics = cls.metrics[classification_type]
        averages = [None, 'binary', 'micro', 'macro', 'samples', 'weighted']
        averages_m = [None, 'micro', 'macro', 'samples', 'weighted']

        if classification_type != 'binary':
            pos_label = None

        if accuracy_score in metrics:
            scores_dict['accuracy'] = accuracy_score(
                                                y_true, y_pred, 
                                                normalize = normalize, 
                                                sample_weight = sample_weights
                                                )

        if f1_score in metrics:
            for average in averages:
                scores_dict['F1'] = f1_score(y_true, y_pred, 
                                             labels = labels, 
                                             pos_label = pos_label, 
                                             average = average, 
                                             sample_weight = sample_weights)
        
        if fbeta_score in metrics and beta is not None:
            f_beta = 'F%s' % str(beta)
            scores_dict[f_beta] = {}
            for average in averages:
                scores_dict[f_beta][str(average)] = fbeta_score(
                                                y_true, y_pred,
                                                beta = beta,
                                                labels = labels,
                                                pos_label = pos_label,
                                                average = average,
                                                sample_weight = sample_weights)


        if hamming_loss in metrics:
            losses_dict['hamming'] = hamming_loss(y_true, y_pred, 
                                                  classes = classes)

        if jaccard_similarity_score in metrics:
            scores_dict['jaccard_similarity_score'] = jaccard_similarity_score(
                                                y_true, y_pred, 
                                                normalize = normalize,
                                                sample_weight = sample_weights
                                                )
        if log_loss in metrics:
            losses_dict['log_loss'] = log_loss(y_true, y_pred, 
                                               eps = eps, 
                                               normalize = normalize, 
                                               sample_weight = sample_weights)
        
        if matthews_corrcoef in metrics:
            scores_dict['matthews_corrcoef'
                        ] = matthews_corrcoef(y_true, y_pred)

        if precision_score in metrics:
            scores_dict['precision'] = {}
            for average in averages:
                scores_dict['Precision'
                            ][average] = precision_score(
                                                y_true, y_pred,
                                                labels = labels,
                                                pos_label = pos_label,
                                                average = average,
                                                sample_weight = sample_weights
                                                )

        if recall_score in metrics:
            scores_dict['recall'] = {}
            for average in averages:
                scores_dict['Recall'][average] = recall_score(
                                                y_true, y_pred,
                                                labels = labels,
                                                pos_label = pos_label,
                                                average = average,
                                                sample_weight = sample_weights
                                                )

        if precision_recall_fscore_support in metrics:
            for average in averages:
                (scores_dict['precision'], 
                 scores_dict['recall'], 
                 scores_dict['f%s' % str(beta)], 
                 scores_dict['support']) = precision_recall_fscore_support(
                                                y_true, y_pred, 
                                                beta = beta, 
                                                labels = labels, 
                                                pos_label = pos_label, 
                                                average = average, 
                                                warn_for = warn_for,
                                                sample_weight = sample_weights
                                                )

        if roc_auc_score in metrics and y_proba is not None:
            scores_dict['roc_auc'] = {}
            for average in averages_m:
                scores_dict['roc_auc'][average] = roc_auc_score(
                                                y_true, y_proba,
                                                average = average,
                                                sample_weight = sample_weights
                                                )
        #TODO: roc_curve
#        if roc_curve in metrics:
#            pass
#        
        if zero_one_loss in metrics:
            losses_dict['zero_one'] = zero_one_loss(
                                                y_true, y_pred,
                                                normalize = normalize,
                                                sample_weight = sample_weights)

        
        if average_precision_score in metrics and y_proba is not None:
            scores_dict['average_precision'] = {}
            for average in averages_m:
                scores_dict['average_precision'
                            ][average] = average_precision_score(
                                                y_true, y_proba,
                                                average = average,
                                                sample_weight = sample_weights)
        
        if confusion_matrix in metrics:
            conf_mat = confusion_matrix(y_true, y_pred,
                                        labels = labels)
            if classes is not None:
                conf_mat = DataFrame(conf_mat, 
                                     index = classes, 
                                     columns = classes)
            scores_dict['confusion_matrix'] = conf_mat
        
        #TODO: hinge_loss
#        if  hinge_loss in metrics:
#            pass
#
#        if precision_recall_curve in metrics:
#            print 'precision_recall_curve'
#            scores

        metrics_dict = {'Scores': scores_dict,
                        'Losses': losses_dict}
        
        return metrics_dict
