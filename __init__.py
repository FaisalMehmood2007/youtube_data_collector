import pandas as pd
import os

def read_all_df(path, show_names=False):
    names = sorted(os.listdir(path))
    print('\n'.join(names))
    all_df = pd.concat([pd.read_csv(path / name) for name in names], axis=0)
    # publisht_timeがあるかどうか
    if 'publishTime' in all_df.columns:
        all_df = all_df.drop_duplicates(subset='video_id').sort_values('publishTime')
    all_df = all_df.reset_index(drop=True)
    print("all shape:", all_df.shape)
    return all_df

def pickup_video_id(df):
    """video_idのみのデータを作成"""
    video_id_list = df['video_id'].unique().tolist()
    print('video_id:', len(video_id_list))
    return video_id_list

