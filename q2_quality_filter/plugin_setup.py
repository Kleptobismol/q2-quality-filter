# ----------------------------------------------------------------------------
# Copyright (c) 2016-2017, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import importlib

import qiime2.plugin
from q2_types.sample_data import SampleData
from q2_types.per_sample_sequences import SequencesWithQuality

import q2_quality_filter
from q2_quality_filter._type import QualityFilterStats
from q2_quality_filter._format import (QualityFilterStatsFmt,
                                       QualityFilterStatsDirFmt)

plugin = qiime2.plugin.Plugin(
    name='quality-filter',
    version=q2_quality_filter.__version__,
    website='https://github.com/wasade/q2-quality-filter',
    package='q2_quality_filter',
    user_support_text=None,
    citation_text=('Quality-filtering vastly improves diversity estimates '
                   'from Illumina amplicon sequencing. Nicholas A Bokulich, '
                   'Sathish Subramanian, Jeremiah J Faith, Dirk Gevers, '
                   'Jeffrey I Gordon, Rob Knight, David A Mills & J Gregory '
                   'Caporaso. Nature Methods 10, 57–59 (2013) '
                   'doi:10.1038/nmeth.2276')
)

plugin.register_formats(QualityFilterStatsFmt, QualityFilterStatsDirFmt)

plugin.register_semantic_types(QualityFilterStats)
plugin.register_semantic_type_to_format(
    QualityFilterStats,
    artifact_format=QualityFilterStatsDirFmt)

plugin.methods.register_function(
    function=q2_quality_filter.q_score,
    inputs={'demux': SampleData[SequencesWithQuality]},
    input_descriptions={
        'demux': 'The per-sample sequence data to quality filter'
    },
    parameters={
        'min_quality': qiime2.plugin.Int,
        'quality_window': qiime2.plugin.Int,
        'min_length_fraction': qiime2.plugin.Float,
        'max_ambiguous': qiime2.plugin.Int
    },

    # descriptions adapted from QIIME 1.9.1's split_libraries_fastq.py
    parameter_descriptions={
        'min_quality': 'The minimum acceptable PHRED score',
        'quality_window': ('The maximum number of low quality base calls to '
                           'observe before truncating'),
        'min_length_fraction': ('The minimum acceptable fraction of sequence '
                                'length after truncation.'),
        'max_ambiguous': ('The maximum number of ambiguous base calls. This '
                          'is applied after quality trimming.')
    },
    outputs=[
        ('filtered_sequences', SampleData[SequencesWithQuality]),
        ('filter_stats', QualityFilterStats)
    ],
    name='Quality filterer',
    description=('This method filters sequence based on quality scores and '
                 'the presence of ambiguous base calls.')
)

plugin.visualizers.register_function(
    function=q2_quality_filter.visualize_stats,
    inputs={'filter_stats': QualityFilterStats},
    input_descriptions={
        'filter_stats': 'Quality filter statistics per sample'
    },
    parameters={},
    name='Visualize filtering stats per sample.',
    description='Display filtering statistics per sample'
)

importlib.import_module('q2_quality_filter._transformer')
