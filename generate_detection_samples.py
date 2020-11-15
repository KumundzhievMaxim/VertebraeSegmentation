# ------------------------------------------
# 
# Program created by Maksim Kumundzhiev
#
#
# email: kumundzhievmaxim@gmail.com
# github: https://github.com/KumundzhievMaxim
# -------------------------------------------

import glob
import sys
import numpy as np
from utility_functions import opening_files
from utility_functions.sampling_helper_functions import densely_label, pre_compute_disks


def generate_samples(dataset_dir, sample_dir,
                     spacing, sample_size,
                     no_of_samples, no_of_zero_samples,
                     file_ext=".nii.gz"):
    sample_size = np.array(sample_size)

    ext_len = len(file_ext)

    paths = glob.glob(dataset_dir + "/**/*" + file_ext, recursive=True)

    np.random.seed(1)

    sample_size_np = np.array(sample_size, int)
    print("Generating " + str(no_of_samples * len(paths)) + " detection samples of size " + str(sample_size_np[0]) +
          " x " + str(sample_size_np[1]) + " x " + str(sample_size_np[2]) + " for " + str(len(paths)) + " scans")

    for cnt, data_path in enumerate(paths):
        data_path_without_ext = data_path[:-ext_len]
        metadata_path = data_path_without_ext + ".lml"

        labels, centroids = opening_files.extract_centroid_info_from_lml(metadata_path)
        centroid_indexes = np.round(centroids / np.array(spacing)).astype(int)

        volume = opening_files.read_nii(data_path, spacing=spacing)

        disk_indices = pre_compute_disks(spacing)
        dense_labelling = densely_label(volume.shape,
                                        disk_indices,
                                        labels,
                                        centroid_indexes,
                                        use_labels=False)
        sample_size_in_pixels = (sample_size / np.array(spacing)).astype(int)

        if volume.shape[0] < sample_size_in_pixels[0]:
            dif = sample_size_in_pixels[0] - volume.shape[0]
            volume = np.pad(volume, ((0, dif), (0, 0), (0, 0)),
                                  mode="constant", constant_values=-5)
            dense_labelling = np.pad(dense_labelling, ((0, dif), (0, 0), (0, 0)),
                                         mode="constant")

        if volume.shape[1] < sample_size_in_pixels[1]:
            dif = sample_size_in_pixels[1] - volume.shape[1]
            volume = np.pad(volume, ((0, 0), (0, dif), (0, 0)),
                                  mode="constant", constant_values=-5)
            dense_labelling = np.pad(dense_labelling, ((0, 0), (0, dif), (0, 0)),
                                         mode="constant")

        if volume.shape[2] < sample_size_in_pixels[2]:
            dif = sample_size_in_pixels[2] - volume.shape[2]
            volume = np.pad(volume, ((0, 0), (0, 0), (0, dif)),
                                  mode="constant", constant_values=-5)
            dense_labelling = np.pad(dense_labelling, ((0, 0), (0, 0), (0, dif)),
                                         mode="constant")

        random_area = volume.shape - sample_size_in_pixels

        name = (data_path.rsplit('/', 1)[-1])[:-ext_len]
        i = 0
        j = 0
        while i < no_of_samples:

            random_factor = np.random.rand(3)
            random_position = np.round(random_area * random_factor).astype(int)
            corner_a = random_position
            corner_b = random_position + sample_size_in_pixels

            sample = volume[corner_a[0]:corner_b[0], corner_a[1]:corner_b[1], corner_a[2]:corner_b[2]]
            labelling = dense_labelling[corner_a[0]:corner_b[0], corner_a[1]:corner_b[1], corner_a[2]:corner_b[2]]

            unique_labels = np.unique(labelling).shape[0]
            if unique_labels > 1 or j < no_of_zero_samples:
                if unique_labels == 1:
                    j += 1
                i += 1

                name_plus_id = name + "-" + str(i)
                path = '/'.join([sample_dir, name_plus_id])
                sample_path = path + "-sample"
                labelling_path = path + "-labelling"
                np.save(sample_path, sample)
                np.save(labelling_path, labelling)

        print(str(cnt + 1) + " / " + str(len(paths)))


generate_samples(dataset_dir=sys.argv[1],
                 sample_dir=sys.argv[2],
                 spacing=(1.0, 1.0, 1.0),
                 sample_size=(64.0, 64.0, 80.0),
                 no_of_samples=5,
                 no_of_zero_samples=1)
