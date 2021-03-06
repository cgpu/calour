# ----------------------------------------------------------------------------
# Copyright (c) 2016--,  Calour development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

from unittest import main
import numpy as np
import pandas as pd
from numpy.testing import assert_array_almost_equal, assert_array_equal

from matplotlib import pyplot as plt

import calour as ca
from calour._testing import Tests
from calour.heatmap.heatmap import _ax_bar, _create_plot_gui


class PlotTests(Tests):
    def setUp(self):
        super().setUp()
        self.test1 = ca.read(self.test2_biom, self.test2_samp, self.test2_feat, normalize=None)

    def test_create_plot_gui(self):
        row, col = 1, 2
        for gui in ('cli', 'qt5', 'jupyter'):
            obs = _create_plot_gui(self.test1, gui=gui, databases=[])
            obs.current_select = row, col
            sid, fid, abd, annt = obs.get_info()
            self.assertListEqual(annt, [])
            self.assertEqual(abd, self.test1.data[row, col])
            self.assertEqual(sid, self.test1.sample_metadata.index[row])
            self.assertEqual(fid, self.test1.feature_metadata.index[col])

    def test_heatmap(self):
        ax = self.test1.heatmap(sample_field='group',
                                feature_field='ph',
                                yticks_max=3)
        obs_images = ax.images
        # test only one heatmap exists
        self.assertEqual(len(obs_images), 1)
        # test heatmap is correct
        assert_array_almost_equal(self.test1.get_data(sparse=False).transpose(),
                                  obs_images[0].get_array())
        obs_lines = ax.lines
        # test only one line exists
        self.assertEqual(len(obs_lines), 1)
        # test the axvline is correct
        assert_array_almost_equal(obs_lines[0].get_xdata(),
                                  np.array([6.5, 6.5]))
        # test axis labels
        self.assertEqual(ax.xaxis.label.get_text(), 'group')
        self.assertEqual(ax.yaxis.label.get_text(), 'ph')
        # test axis tick labels
        obs_xticklabels = [i.get_text() for i in ax.xaxis.get_ticklabels()]
        self.assertListEqual(obs_xticklabels, ['1', '2'])
        # remove the 1st and last ticks because they are only the bounds
        obs_yticks = ax.get_yticks()[1:-1]
        # assert the tick locations are the same
        assert_array_equal(obs_yticks, np.array([0., 3., 6.]))

    def test_ax_bar(self):
        fig, ax = plt.subplots()
        colors = pd.Series({'a': (1.0, 0.0, 0.0, 1),
                            'b': (0.0, 0.5, 0.0, 1)})
        axes = _ax_bar(ax, ['a', 'a', 'b'], colors, 0.3, 0)
        self.assertIs(ax, axes)

        # test face color rectangle in the bar
        self.assertListEqual(
            [i.get_facecolor() for i in axes.patches],
            list(colors.values))
        # test the position rectangle in the bar
        self.assertListEqual(
            [i.get_xy() for i in axes.patches],
            [(-0.5, 0), (1.5, 0)])
        # test the texts in each rectangle in the bar
        self.assertListEqual(
            [i.get_text() for i in axes.texts],
            ['a', 'b'])


if __name__ == '__main__':
    main()
