import pandas as pd

# Read files
df_d5 = pd.read_csv('data/Q5/Q5.maryphilip_DEG_day5_group_L5_vs_E5.csv')
df_d7 = pd.read_csv('data/Q5/Q5.maryphilip_DEG_day7_group_L7_vs_E7.csv')

# Rename 'Unnamed: 0' to 'Gene' for convenience
df_d5 = df_d5.rename(columns={'Unnamed: 0': 'Gene'})
df_d7 = df_d7.rename(columns={'Unnamed: 0': 'Gene'})

# Filter for significant genes (padj < 0.05)
sig_d5 = df_d5[df_d5['padj'] < 0.05]
sig_d7 = df_d7[df_d7['padj'] < 0.05]

# Top Upregulated in L (Exhaustion)
top_L5 = sig_d5.sort_values(by='log2FoldChange', ascending=False).head(10)
top_L7 = sig_d7.sort_values(by='log2FoldChange', ascending=False).head(10)

# Top Upregulated in E (Effector)
top_E5 = sig_d5.sort_values(by='log2FoldChange', ascending=True).head(10)
top_E7 = sig_d7.sort_values(by='log2FoldChange', ascending=True).head(10)

print("Top Genes Upregulated in L5 (Early Exhaustion):")
print(top_L5[['Gene', 'log2FoldChange', 'padj']].to_string(index=False))

print("Top Genes Upregulated in L7 (Established Exhaustion):")
print(top_L7[['Gene', 'log2FoldChange', 'padj']].to_string(index=False))

# Check specific markers
markers = ['Pdcd1', 'Havcr2', 'Tox', 'Tcf7', 'Lag3', 'Ctla4', 'Entpd1', 'Cd200', 'Cd160']
print("Specific Markers in L5 vs E5:")
print(df_d5[df_d5['Gene'].isin(markers)][['Gene', 'log2FoldChange', 'padj', 'meanTPM_L5', 'meanTPM_E5']].to_string(index=False))
print("Specific Markers in L7 vs E7:")
print(df_d7[df_d7['Gene'].isin(markers)][['Gene', 'log2FoldChange', 'padj', 'meanTPM_L7', 'meanTPM_E7']].to_string(index=False))